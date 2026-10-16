import * as pixel from './pixellab-character.js';
import * as render from './render3d-character.js';
let current='3d';const sources={pixel, '3d':render};
export const SLOTS={},DEFAULT_OUTFIT={},ACTIONS={};
function sync(){for(const [target,source]of [[SLOTS,sources[current].SLOTS],[DEFAULT_OUTFIT,sources[current].DEFAULT_OUTFIT],[ACTIONS,sources[current].ACTIONS]]){for(const k of Object.keys(target))delete target[k];Object.assign(target,source);}}
export async function loadArt(){await sources[current].loadArt();sync();}
export async function setArtSource(source){await sources[source].loadArt();current=source;sync();}
export const artSource=()=>current;
export const progressForFrame=(mode,index)=>sources[current].progressForFrame(mode,index);
export class PaperDoll{constructor(){this.source='';this.impl=null;}draw(...args){if(this.source!==current){this.impl=new sources[current].PaperDoll();this.source=current;}const result=this.impl.draw(...args);this.layers=this.impl.layers;return result;}}
