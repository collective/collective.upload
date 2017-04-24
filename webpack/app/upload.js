import './upload.less';
import './upload-icon.png';

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
    this.bindEvents();
    if (this.$el.length > 0) {
      this.initFileUpload();
    }

    this.exif = {};
    this.exif.ImageDescription = 0x010E;
    this.exif.Artist = 0x013B;
  }

  /**
   * Refresh elements (needed when open modal)
   */
  refresh() {
    // if overlay is open at /folder_contents page, pick the overlay fileuploader
    this.$el = $('.fileupload').last();
  }

  /**
   * Bind events
   */
  bindEvents() {
    //overlay
    $('#plone-contentmenu-factories #multiple-files').prepOverlay({
      subtype: 'ajax',
      config: {
        onLoad: $.proxy(this.initFileUpload, this),
        onBeforeClose: this.reloadPage
      }
    });
    $(document).on('drop dragover', (e) => {
      // Prevent the default browser drop action:
      e.preventDefault();
    });
    $(document).on('drop', $.proxy(this.crossSiteDrop, this));
    $(document).on('click', '.template-upload button.cancel', $.proxy(this.cancelOne, this));
    $(document).on('click', '.fileupload-buttonbar button.cancel', $.proxy(this.cancelAll, this));
  }

  /**
   * Initiate fileupload plugin
   */
  initFileUpload() {
    // Overlay requires to refresh element object
    this.refresh();
    let options = this.$el.prop('dataset');
    let filesRE = new RegExp('(\\.|\/)('+options.extensions+')$', 'i');

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
      acceptFileTypes: filesRE,
      process: [
        {
          action: 'load',
          fileTypes: filesRE,
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
    }).on(
      'fileuploadprocessdone', $.proxy(this.extractMetadata, this)
    ).on(
      'fileuploadprogress', $.proxy(this.finishUpload, this)
    ).on(
      'fileuploadprogressall', $.proxy(this.finishAllUpload, this)
    );
  }

  /**
   * Decode UTF8 string to Unicode
   * http://stackoverflow.com/a/13691499
   * @param {s} string - String to decode
   */
  decodeUTF8(s) {
    return decodeURIComponent(escape(s));
  }

  /**
   * Extract image metadata using EXIF
   * @param {e} event - jQuery event variable
   * @param {data} data - Image data
   */
  extractMetadata(e, data) {
    if (typeof data.exif === 'undefined') {
      return;
    }
    let description = data.exif[this.exif.ImageDescription];
    if (typeof description !== 'undefined') {
      description = this.decodeUTF8(description);
      $('.description', data.context[0]).val(description);
    }
    let artist = data.exif[this.exif.Artist];
    if (typeof artist !== 'undefined') {
      artist = this.decodeUTF8(artist);
      $('.rights', data.context[0]).val(artist);
    }
  }

  /**
   * Check if using Bootstrap 2
   * http://stackoverflow.com/a/14768682
   * This method is needed as workaround for old bootstrap version conflict
   */
  hasBootstrap2() {
    let hasBootstrap = (typeof $().modal == 'function');
    let hasBootstrap3 = (typeof $().emulateTransitionEnd === 'function');
    return (hasBootstrap && !hasBootstrap3);
  }

  /**
   * Cancell all files added
   * This callback is needed as workaround for old bootstrap version conflict
   * @param {e} event - jQuery event variable
   */
  cancelAll(e) {
    this.reloadPage();
    if (!this.hasBootstrap2()) {
      return;
    }
    $('.template-upload').remove();
  }

  /**
   * Cancell one file added
   * This callback is needed as workaround for old bootstrap version conflict
   * @param {e} event - jQuery event variable
   */
  cancelOne(e) {
    this.reloadPage();
    if (!this.hasBootstrap2()) {
      return;
    }
    $(e.target).parents('.template-upload').remove();
  }

  /**
   * Method copied from jquery.fileupload implementation
   * This callback is needed as workaround for old bootstrap version conflict
   * @param {bytes} bytes - Size of file in bytes
   */
  formatFileSize(bytes) {
    if (typeof bytes !== 'number') {
      return '';
    }
    if (bytes >= 1000000000) {
      return (bytes / 1000000000).toFixed(2) + ' GB';
    }
    if (bytes >= 1000000) {
      return (bytes / 1000000).toFixed(2) + ' MB';
    }
    return (bytes / 1000).toFixed(2) + ' KB';
  }

  /**
   * Called when finish one file upload
   * This callback is needed as workaround for old bootstrap version conflict
   * @param {e} event - jQuery event variable
   * @param {data} data - Progress data
   */
  finishUpload(e, data) {
    if (!this.hasBootstrap2()) {
      return;
    }
    let progress = parseInt(data.loaded / data.total * 100, 10);
    if (progress !== 100) {
      return;
    }
    // render template
    let $html = $(data.downloadTemplate({
      files: data.files,
      formatFileSize: this.formatFileSize,
      options: data
    }));
    // update html
    data.context.replaceWith($html);
    // render preview
    $html.find('.preview').each(function (index, elm) {
      $(elm).append(data.files[index].preview);
    });
  }

  /**
   * Called when finish all uploads
   * @param {e} event - jQuery event variable
   * @param {data} data - Progress data
   */
  finishAllUpload(e, data) {
    let progress = parseInt(data.loaded / data.total * 100, 10);
    if (progress !== 100) {
      return;
    }
    this.reloadPage();
  }

  /**
   * Drop image from other website page
   * @param {e} event - jQuery event variable
   */
  crossSiteDrop(e) {
    if (typeof e.originalEvent.dataTransfer === 'undefined') {
      return;
    }
    // Google Chrome
    let url = $(e.originalEvent.dataTransfer.getData('text/html')).filter('img').attr('src');
    // Firefox
    if (typeof url === 'undefined') {
      url = e.originalEvent.dataTransfer.getData('text/x-moz-url').split('\n')[0];
    }
    if (typeof url === 'undefined') {
      return;
    }
    // JavaScript URL parser: https://gist.github.com/jlong/2428561
    let parser = document.createElement('a');
    parser.href = location.href;
    parser.pathname = parser.pathname.replace(/\/folder_contents*|\/view*/, '');
    parser.pathname = parser.pathname + '/@@jsonimageserializer';
    $.ajax({
      url: parser.href,
      data: {url: url},
      context: this,
      success: (data) => {
        let img = document.createElement('img');
        img.name = data.name;
        img.onload = $.proxy((e) => {
          let canvas = document.createElement('canvas');
          canvas.width = img.width;
          canvas.height = img.height;
          if (canvas.getContext && canvas.toBlob) {
            canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height);
            canvas.toBlob(function(that, name) {
              return (blob) => {
                blob.name = name;
                that.$el.fileupload('add', {files: [blob]});
              };
            }(this, img.name), 'image/jpeg');
          }
        }, this);
        img.src = data.data;
      }
    });
  }
  /**       
   * Reload page when close overlay     
   * @param {e} event - jQuery event variable       
   */       
  reloadPage(e) {       
    // reload page if all uploads finish
    let $uploads = $('.template-upload', this.$el);
    if ($uploads.length === 0 || $('.progress', $uploads).attr('aria-valuenow') === '100') {
      location.reload();
    }
  }
}


$(() => {
  new Upload();
});


module.exports = Upload;
