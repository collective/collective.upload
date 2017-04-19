import './upload.less';
import './upload-icon.png';

import 'get-image-data/jquery.getimagedata.js';
import 'blueimp-tmpl/js/tmpl.js';
import 'blueimp-load-image/js/index.js';
import 'blueimp-canvas-to-blob/js/canvas-to-blob.js';
import 'blueimp-file-upload/js/jquery.iframe-transport.js';
import 'blueimp-file-upload/js/jquery.fileupload.js';
import 'blueimp-file-upload/js/jquery.fileupload-process.js';
import 'blueimp-file-upload/js/jquery.fileupload-image.js';
import 'blueimp-file-upload/js/jquery.fileupload-audio.js';
import 'blueimp-file-upload/js/jquery.fileupload-video.js';
import 'blueimp-file-upload/js/jquery.fileupload-validate.js';
import 'blueimp-file-upload/js/jquery.fileupload-ui.js';


class Upload {
  /**
   * Create file upload object and bind events
   * @constructor
   */
  constructor() {
    this.refresh();
    this.bind_events();
    if (this.$el.length > 0) {
      this.init_fileupload();
    }
  }

  /**
   * Refresh elements (needed when open modal)
   */
  refresh() {
    this.$el = $('.fileupload');
  }

  /**
   * Bind events
   */
  bind_events() {
    //overlay
    $('#plone-contentmenu-factories #multiple-files').prepOverlay({
      subtype: 'ajax',
      config: {
        onLoad: $.proxy(this.init_fileupload, this)
      }
    });
    $(document).on('drop dragover', (e) => {
      // Prevent the default browser drop action:
      e.preventDefault();
    });
    $(document).on('drop', this.cross_site_drop);
    $(document).on('click', '.fileupload-buttonbar button.cancel', this.cancel_all);
    $(document).on('click', '.template-upload button.cancel', this.cancel_one);
  }

  /**
   * Initiate fileupload plugin
   */
  init_fileupload() {
    // Overlay requires to refresh element object
    this.refresh();
    let options = this.$el.prop('dataset');
    let files_re = new RegExp('(\\.|\/)('+options.extensions+')$', 'i');

    // Map tranlations options to object
    let translations = {};
    for (let k in options) {
      if (/^translations/.test(k)) {
        let newk = k.substring('translations'.length);
        newk = newk.charAt(0).toLowerCase() + newk.substring(1);
        translations[newk] = options[k];
      }
    }

    // Initialize the jQuery File Upload widget:
    this.$el.fileupload({
      sequentialUploads: true,
      singleFileUploads: true
    }).fileupload('option', {
      // Enable image resizing, except for Android and Opera,
      // which actually support image resizing, but fail to
      // send Blob objects via XHR requests:
      disableImageResize: /Android(?!.*Chrome)|Opera/.test(window.navigator.userAgent),
      maxFileSize: options.maxFileSize,
      acceptFileTypes: files_re,
      process: [
        {
          action: 'load',
          fileTypes: files_re,
          maxFileSize: options.maxFileSize
        },
        {
          action: 'resize',
          maxWidth: options.resizeMaxWidth,
          maxHeight: options.resizeMaxHeight
        },
        {
          action: 'save'
        }
      ],
      messages: translations
    });
  }

  /**
   * Cancell all files added
   * This callback is needed as workaround for old bootstrap version conflict
   * @param {e} event - jQuery event variable
   */
  cancel_all(e) {
    $('.template-upload').remove();
  }

  /**
   * Cancell one file added
   * This callback is needed as workaround for old bootstrap version conflict
   * @param {e} event - jQuery event variable
   */
  cancel_one(e) {
    $(e.target).parents('.template-upload').remove();
  }

  /**
   * Drop image from other website page
   * @param {e} event - jQuery event variable
   */
  cross_site_drop(e) {
    // Google Chrome
    let url = $(e.originalEvent.dataTransfer.getData('text/html')).filter('img').attr('src');
    // Firefox
    if (typeof(url) === 'undefined') {
      url = e.originalEvent.dataTransfer.getData('text/x-moz-url').split('\n')[0];
    }
    if (typeof(url) === 'undefined') {
      return;
    }
    // JavaScript URL parser: https://gist.github.com/jlong/2428561
    let parser = document.createElement('a');
    parser.href = location.href;
    parser.pathname = parser.pathname.replace(/\/folder_contents*|\/view*/, '');
    parser.pathname = parser.pathname + '/@@jsonimageserializer';
    $.getImageData({
      url: url,
      server: parser.href,
      success: (img) => {
        let canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        if (canvas.getContext && canvas.toBlob) {
          canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height);
          canvas.toBlob((blob) => {
            $('.fileupload').fileupload('add', {files: [blob]});
          }, "image/jpeg");
        }
      }
    });
  }
}


$(function () {
  new Upload();
});


module.exports = Upload;
