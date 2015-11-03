/**
 * editor module
 * @author victor li
 * @date 2015/11/03
 */

'use strict'

require('expose?$!expose?jQuery!jquery');
const converter = new Markdown.Converter();
const editor = new Markdown.Editor(converter);
editor.run();

$('body').on('click', '.switch-editor-mode', function(e) {
    const mode = $(this).data('mode');
    $('.switch-editor-mode').removeClass('active');
    $(this).addClass('active');
    if (mode === 'edit') {
        $('.editor-preview').hide();
        $('.editor-area').show();
    } else if (mode === 'preview') {
        $('.editor-area').hide();
        $('.editor-preview').show();
    }
});
