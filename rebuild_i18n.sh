#! /bin/sh

I18NDOMAIN="collective.upload"

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
bin/i18ndude rebuild-pot --pot src/collective/upload/locales/${I18NDOMAIN}.pot \
    --create ${I18NDOMAIN} \
   src/collective/upload

# Synchronise the resulting .pot with all .po files
for po in src/collective/upload/locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    bin/i18ndude sync --pot src/collective/upload/locales/${I18NDOMAIN}.pot $po
done
