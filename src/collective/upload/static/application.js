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


/*global $, window, document */
(function ($) {
var fileUploadErrors = {};
$.widget('blueimpUIX.fileupload', $.blueimpUI.fileupload, {

    _renderTemplate: function (func, files) {
        return func({
            files: files,
            formatFileSize: this._formatFileSize,
            options: this.options
        });
    },

    _initTemplates: function () {
        this.options.uploadTemplate = function (o) {
            var rows = $();
            $.each(o.files, function (index, file) {
                var row = $('<tr class="template-upload">' +
                    '<td class="preview"><span class="fade"></span></td>' +
                    '<td class="name"><input name="title[]" type="text" required/><br/><label for="description">Descripción</label><textarea name="description[]" cols="10" rows="3"></textarea></td>' +
                    '<td class="size"></td>' +
                    (file.error ? '<td class="error" colspan="2"></td>' :
                            '<td class="progress"><div class="progressbar">' +
                                '<div style="width:0%;"></div></div></td>' +
                                '<td class="start"><button class="btn primary">'+jupload.messages['START_MSG']+'</button></td>'
                    ) + '<td class="cancel"><button class="btn info">Cancel</button></td></tr>');
                row.find('.name input').val(file.name);
                row.find('.size').text(o.formatFileSize(file.size));
                if (file.error) {
                    row.addClass('ui-state-error');
                    row.find('.error').text(
                        fileUploadErrors[file.error] || file.error
                    );
                }
                rows = rows.add(row);
            });
            return rows;
        };
        this.options.downloadTemplate = function (o) {
            var rows = $();
            $.each(o.files, function (index, file) {
                var row = $('<tr class="template-download">' +
                    (file.error ? '<td></td><td class="name"></td>' +
                        '<td class="size"></td><td class="error" colspan="2"></td>' :
                            '<td class="preview"></td>' +
                                '<td class="name"><a></a><br/><p></p></td>' +
                                '<td class="size"></td><td colspan="2"></td>'
                    ) + '<td class="delete"><button class="btn danger">'+jupload.messages['DELETE_MSG']+'</button> ' +
                        '<input type="checkbox" name="delete" value="1"></td></tr>');
                row.find('.size').text(o.formatFileSize(file.size));
                if (file.error) {
                    row.find('.name').text(file.title);
                    row.addClass('ui-state-error');
                    row.find('.error').text(
                        fileUploadErrors[file.error] || file.error
                    );
                } else {
                    row.find('.name a').text(file.title);
                    row.find('.name p').text(file.description);
                    if (file.thumbnail_url) {
                        row.find('.preview').append('<a><img></a>')
                            .find('img').prop('src', file.thumbnail_url);
                        row.find('a').prop('rel', 'gallery');
                    }
                    row.find('a').prop('href', file.url);
                    row.find('.delete button')
                        .attr('data-type', file.delete_type)
                        .attr('data-url', file.delete_url);
                }
                rows = rows.add(row);
            });
            return rows;
        };
    }

});
}(j$));


j$(document).ready(function() {
    var $ = j$;
  // Handler for .ready() called.
    config_upload_form  = function () {
    'use strict';

        //we have to check if the fileupload element existing
        
        if ($('#fileupload')[0] !== undefined) {
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

            // main settings:
            var files_re = new RegExp('(\\.|\/)('+jupload.config['extensions']+')$', 'i');
            $('#fileupload').fileupload('option', {
                maxFileSize: jupload.config['max_file_size'],
                acceptFileTypes: files_re,
                resizeMaxWidth: jupload.config['resize_max_width'],
                resizeMaxHeight: jupload.config['resize_max_height']
            });
            // Upload server status check for browsers with CORS support:
            if ($.support.cors) {
                $.ajax({
                    url:'',
                    type: 'HEAD'
                }).fail(function () {
                    $('<span class="alert alert-error"/>')
                        .text('Upload server currently unavailable - ' +
                                new Date())
                        .appendTo('#fileupload');
                });
            }

            //in the latest version we have a method formData who actually is 
            // doing this...=)
            $('#fileupload').bind('fileuploadsubmit', function (e, data) {
                var inputs = data.context.find(':input');
                if (inputs.filter('[required][value=""]').first().focus().length) {
                    return false;
                }
                data.formData = inputs.serializeArray();
            });            
            
        }

    };
    config_upload_form();
});
