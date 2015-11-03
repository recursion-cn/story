/**
 * editor module
 * @author victor li
 * @date 2015/11/03
 */

'use strict'

const converter = new Markdown.Converter();
const editor = new Markdown.Editor(converter);
editor.run();
