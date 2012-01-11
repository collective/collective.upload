jq(function () {
    //first we have to add a new action in the add new menu
    var link = $('<li><a href="./@@media_uploader" class="contenttype-multiplefiles" id="multiplefiles" title=""><img width="16" height="16" alt="" src="++resource++collective.upload/document_small_upload.png" title="multiplefiles"><span class="subMenuTitle">Upload multiple files or images</span></a></li>');
    jq('#plone-contentmenu-factories .actionMenuContent ul').append(link);
    
    //overlay
    jq('#multiplefiles').prepOverlay(
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
