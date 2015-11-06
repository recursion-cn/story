/**
 * app entry
 *
 * @author victor li
 * @date 2015/11/01
 */

'use strict'

require('expose?$!expose?jQuery!jquery');

$('body').on('mouseover', '.nav-user-panel', function() {
    $(this).find('.user-panel').fadeIn();
}).on('mouseleave', '.nav-user-panel', function() {
    $(this).find('.user-panel').fadeOut();
});