const makeConfig = require('sc-recipe-staticresources');


module.exports = makeConfig(
  // name
  'collective.upload',

  // shortName
  'upload',

  // path
  `${__dirname}/../src/collective/upload/browser/static`,

  //publicPath
  '++resource++collective.upload/',

  //callback
  function(config, options) {
    config.entry.unshift(
      './app/img/upload-icon.png',
    );
    config.resolve = {
      alias: {
        'canvas-to-blob': 'blueimp-canvas-to-blob/js/canvas-to-blob.js',
        'jquery-ui/ui/widget': 'blueimp-file-upload/js/vendor/jquery.ui.widget.js',
        'load-image': 'blueimp-load-image/js/load-image.js',
        'load-image-exif': 'blueimp-load-image/js/load-image-exif.js',
        'load-image-meta': 'blueimp-load-image/js/load-image-meta.js',
        'load-image-scale': 'blueimp-load-image/js/load-image-scale.js'
      }
    };
  },
);
