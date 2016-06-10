/*
 * jQuery File Upload Plugin JS Example 6.0
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

$(document).ready(function() {
  // Handler for .ready() called.
    config_upload_form  = function () {
    'use strict';

        //we have to check if the fileupload element existing

        if ($('#fileupload')[0] !== undefined) {
            var files_re = new RegExp('(\\.|\/)('+jupload.config['extensions']+')$', 'i');
            // Initialize the jQuery File Upload widget:
            $('#fileupload').fileupload({'sequentialUploads':true, 'singleFileUploads':true});

            // Enable iframe cross-domain access via redirect option:
            $('#fileupload').fileupload(
                'option',
                'redirect',
                window.location.href.replace(
                    /\/[^\/]*$/,
                    '/cors/result.html?%s'
                )
            );

            $('#fileupload').fileupload('option', {
                url: '',
                maxFileSize: jupload.config['max_file_size'],
                acceptFileTypes: files_re,
                process: [
                    {
                        action: 'load',
                        fileTypes: files_re,
                        maxFileSize: jupload.config['max_file_size']
                    },
                    {
                        action: 'resize',
                        maxWidth: jupload.config['resize_max_width'],
                        maxHeight: jupload.config['resize_max_height']
                    },
                    {
                        action: 'save'
                    }
                ],
                start_i18n: jupload.messages['START_MSG'],
                cancel_i18n: jupload.messages['CANCEL_MSG'],
                delete_i18n: jupload.messages['DELETE_MSG'],
                description_i18n: jupload.messages['DESCRIPTION_MSG'],
                error_i18n: jupload.messages['ERROR_MSG']
            });
            // Upload server status check for browsers with CORS support:
            if ($.support.cors) {
                $.ajax({
                    url: './',
                    type: 'HEAD'
                }).fail(function () {
                    $('<span class="alert alert-error"/>')
                        .text('Upload server currently unavailable - ' +
                                new Date())
                        .appendTo('#fileupload');
                });
            }

            $('#fileupload').bind('fileuploadsubmit', function (e, data) {
                var inputs;
                if(data.context){
                    inputs = data.context.find(':input');
                }else{
                    inputs = data.form.find(':input');
                }
                if (inputs.filter('[required][value=""]').first().focus().length) {
                    return false;
                }
                data.formData = inputs.serializeArray();
            });

            $(document).bind('drop', function (e) {
              e.preventDefault();
              var upload_image = function(img) {
                var canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height);
                canvas.toBlob(function (blob) {
                  $('#fileupload').fileupload('add', {files: [blob]});
                }, "image/jpeg");
              };
              // drop multiple files from file system
              var file, i, len, ref;
              ref = e.originalEvent.dataTransfer.files;
              for (i = 0, len = ref.length; i < len; i++) {
                file = ref[i];
                var reader = new FileReader();
                reader.onload = function(e) {
                  var img = new Image();
                  img.onload = function() {
                    upload_image(this);
                  };
                  img.src = e.target.result;
                }
                reader.readAsBinaryString(file);
              }
              // drop one file from other site
              var url = $('img', e.originalEvent.dataTransfer.getData('text/html')).attr('src');
              if (url) {
                // JavaScript URL parser: https://gist.github.com/jlong/2428561
                var parser = document.createElement('a');
                parser.href = location.href;
                parser.pathname = parser.pathname.replace(/\/folder_contents*|\/view*/, '');
                parser.pathname = parser.pathname + '/@@jsonimageserializer';
                parser.search = 'callback=?';
                $.getImageData({
                  url: url,
                  server: parser.href,
                  success: upload_image
                });
              }
            });
        }
    };
    config_upload_form();

    //overlay
    $('#plone-contentmenu-factories #multiple-files').prepOverlay(
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
