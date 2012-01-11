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

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

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
                    '<td class="name"></td>' +
                    '<td class="size"></td>' +
                    (file.error ? '<td class="error" colspan="2"></td>' :
                            '<td class="progress"><div class="progressbar">' +
                                '<div style="width:0%;"></div></div></td>' +
                                '<td class="start"><button class="btn primary">Start</button></td>'
                    ) + '<td class="cancel"><button class="btn info">Cancel</button></td></tr>');
                row.find('.name').text(file.name);
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
                                '<td class="name"><a></a></td>' +
                                '<td class="size"></td><td colspan="2"></td>'
                    ) + '<td class="delete"><button class="btn danger">Delete</button> ' +
                        '<input type="checkbox" name="delete" value="1"></td></tr>');
                row.find('.size').text(o.formatFileSize(file.size));
                if (file.error) {
                    row.find('.name').text(file.name);
                    row.addClass('ui-state-error');
                    row.find('.error').text(
                        fileUploadErrors[file.error] || file.error
                    );
                } else {
                    row.find('.name a').text(file.name);
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


$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload(
        {
            'sequentialUploads':true,
            dragover: function (e, data) {
                console.log('darg');
            }
        }
    )

    // Load existing files:
    $.getJSON($('#fileupload').prop('action'), function (files) {
        var fu = $('#fileupload').data('fileupload'),
            template;
        fu._adjustMaxNumberOfFiles(-files.length);
        template = fu._renderDownload(files)
            .appendTo($('#fileupload .files'));
        // Force reflow:
        fu._reflow = fu._transition && template.length &&
            template[0].offsetWidth;
        template.addClass('in');
    });


    // Enable iframe cross-domain access via redirect page:
    var redirectPage = window.location.href.replace(
        /\/[^\/]*$/,
        '/result.html?%s'
    );
    $('#fileupload').bind('fileuploadsend', function (e, data) {
        if (data.dataType.substr(0, 6) === 'iframe') {
            var target = $('<a/>').prop('href', data.url)[0];
            if (window.location.host !== target.host) {
                data.formData.push({
                    name: 'redirect',
                    value: redirectPage
                });
            }
        }
    });

    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files').delegate(
        'a:not([rel^=gallery])',
        'click',
        function (e) {
            e.preventDefault();
            $('<iframe style="display:none;"></iframe>')
                .prop('src', this.href)
                .appendTo(document.body);
        }
    );

});
