jq(function () {
    //overlay
    jq('#plone-contentmenu-factories #collective-upload').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            config: {
                onLoad: function(arg){
                    config_upload_form();
                }
            }
        }
    );
});
