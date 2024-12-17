# MATLAB Codebase Summary

Generated on: 2024-12-16 22:28:21


## Summary Statistics
- Total MATLAB files: 110
- Total functions: 368

---
Base directory: /Users/Adam/Desktop/co/projects/ISI

## Root Directory
### getMagFactors.m
**File Statistics:**
- Total lines: 22
- Non-empty lines: 15
- Number of functions: 1
**Functions:**
```matlab
function [JacIm prefAxisMF Distrtion] = getMagFactors(kmap_hor,kmap_vert,pixpermm)
```
---
### getPatchSign.m
**File Statistics:**
- Total lines: 11
- Non-empty lines: 10
- Number of functions: 1
**Functions:**
```matlab
function [patchSign areaSign] = getPatchSign(im,imsign)
```
---
### phi.m
**File Statistics:**
- Total lines: 10
- Non-empty lines: 7
- Number of functions: 1
**Functions:**
```matlab
function [B] = phi(A)
```
---
### getMouseAreaBorders.m
**File Statistics:**
- Total lines: 294
- Non-empty lines: 218
- Number of functions: 1
**Functions:**
```matlab
function im = getAreaBorders(anim,alt_expt,azi_expt,pixpermm)
```
---
### getMouseAreasX.m
**File Statistics:**
- Total lines: 393
- Non-empty lines: 285
- Number of functions: 4
**Functions:**
```matlab
function im = getMouseAreasX(kmap_hor,kmap_vert,pixpermm)
function imout = ploteccmap(im,rng,pixpermm)
function imout = plotehorvertmap(im,rng)
function [patchSign areaSign] = getPatchSign(im,imsign)
```
---
### overRep.m
**File Statistics:**
- Total lines: 0
- Non-empty lines: 0
- Number of functions: 0
---
### fusePatchesX.m
**File Statistics:**
- Total lines: 240
- Non-empty lines: 180
- Number of functions: 3
**Functions:**
```matlab
function [im fuseflag] = fusePatchesX(im,kmap_hor,kmap_vert,pixpermm)
function [spCov JacCoverage ActualCoverage MagFac] = overRep(kmap_hor,kmap_vert,U,Jac,patch,sphdom,sphX,pixpermm)
function imout = ploteccmap(im,rng,pixpermm)
```
---
### getAreaBorders.m
**File Statistics:**
- Total lines: 403
- Non-empty lines: 306
- Number of functions: 1
**Functions:**
```matlab
function getAreaBorders(anim,alt_expt,azi_expt)
```
---
### plotmap.m
**File Statistics:**
- Total lines: 53
- Non-empty lines: 37
- Number of functions: 1
**Functions:**
```matlab
function imout = plotmap(im,rng,pixpermm)
```
---
### getRadialEccMapX.m
**File Statistics:**
- Total lines: 57
- Non-empty lines: 38
- Number of functions: 1
**Functions:**
```matlab
function AreaInfo = getRadialEccMapX(kmap_hor,kmap_vert)
```
---
### getPatchCoM.m
**File Statistics:**
- Total lines: 40
- Non-empty lines: 30
- Number of functions: 1
**Functions:**
```matlab
function [CoMxy Axisxy] = getPatchCoM(imseg)
```
---
### plotehorvertmap.m
**File Statistics:**
- Total lines: 46
- Non-empty lines: 34
- Number of functions: 1
**Functions:**
```matlab
function imout = plotehorvertmap(im,rng)
```
---
### getV1id.m
**File Statistics:**
- Total lines: 13
- Non-empty lines: 11
- Number of functions: 1
**Functions:**
```matlab
function [V1id ids V1map] = getV1id(im)
```
---
### ploteccmap.m
**File Statistics:**
- Total lines: 43
- Non-empty lines: 31
- Number of functions: 1
**Functions:**
```matlab
function imout = ploteccmap(im,rng,pixpermm)
```
---
### smoothPatchesX.m
**File Statistics:**
- Total lines: 28
- Non-empty lines: 18
- Number of functions: 1
**Functions:**
```matlab
function mapout = smoothPatchesX(map,im)
```
---
### splitPatchesX.m
**File Statistics:**
- Total lines: 398
- Non-empty lines: 277
- Number of functions: 6
**Functions:**
```matlab
function im = splitPatchesX(im,kmap_hor,kmap_vert,kmap_rad,pixpermm)
function [spCov JacCoverage ActualCoverage MagFac] = overRep(kmap_hor,kmap_vert,U,Jac,patch,sphdom,sphX,pixpermm)
function [im splitflag Npatch] = resetPatch(im,centerPatch,imlab,q)
function centerPatch = getCenterPatch(kmap_rad,im,R)
function [Nmin minpatch newpatches rad] = getNlocalmin(idpatch,Rmax,kmap_rad)
function imout = ploteccmap(im,rng,DS,pixpermm)
```
---

## Directory: regImages
### imgtrxrun.m
**File Statistics:**
- Total lines: 45
- Non-empty lines: 37
- Number of functions: 1
**Functions:**
```matlab
function [img_out, LT, ref_out_hat] = imgtrxrun(ref_in,ref_out,img_in,input_points,base_points)
```
---
### regImages.m
**File Statistics:**
- Total lines: 177
- Non-empty lines: 144
- Number of functions: 8
**Functions:**
```matlab
function varargout = regImages(varargin)
function regImages_OpeningFcn(hObject, eventdata, handles, varargin)
function varargout = regImages_OutputFcn(hObject, eventdata, handles)
function saveImgpath_Callback(hObject, eventdata, handles)
function saveImgpath_CreateFcn(hObject, eventdata, handles)
function LoadImagesButton_Callback(hObject, eventdata, handles)
function SelectRefPoints_Callback(hObject, eventdata, handles)
function TransformButton_Callback(hObject, eventdata, handles)
```
---

## Directory: Utilities
### overlaymaps_old2.m
**File Statistics:**
- Total lines: 699
- Non-empty lines: 643
- Number of functions: 1
**Functions:**
```matlab
function overlaymaps_old2(anim,expt,AltAz)
```
---
### plotISImaps.m
**File Statistics:**
- Total lines: 357
- Non-empty lines: 309
- Number of functions: 1
**Functions:**
```matlab
function plotISImaps
```
---
### RetFigures.m
**File Statistics:**
- Total lines: 115
- Non-empty lines: 92
- Number of functions: 1
**Functions:**
```matlab
function RetFigures
```
---
### Gprocesskret_batch.m
**File Statistics:**
- Total lines: 92
- Non-empty lines: 75
- Number of functions: 1
**Functions:**
```matlab
function [kmap_hor kmap_vert delay_hor delay_vert magS] = Gprocesskret_batch(f1,bw,hl,hh)
```
---
### kenta_overlay.m
**File Statistics:**
- Total lines: 675
- Non-empty lines: 619
- Number of functions: 1
**Functions:**
```matlab
function kenta_overlay(anim,expt,AltAz,grabnum)
```
---
### anatomyoverlay.m
**File Statistics:**
- Total lines: 319
- Non-empty lines: 264
- Number of functions: 1
**Functions:**
```matlab
function anatomyoverlay(anim,AzExpt,AltExpt)
```
---
### Script_mg.m
**File Statistics:**
- Total lines: 129
- Non-empty lines: 106
- Number of functions: 0
**File Description:**
Script for analyzing kalatsky retinotopy with 2photon data
---
### smoothF0.m
**File Statistics:**
- Total lines: 25
- Non-empty lines: 20
- Number of functions: 0
---
### overlaymaps_6_12.m
**File Statistics:**
- Total lines: 699
- Non-empty lines: 643
- Number of functions: 1
**Functions:**
```matlab
function overlaymaps(anim,expt,AltAz)
```
---
### HorizRet.m
**File Statistics:**
- Total lines: 79
- Non-empty lines: 68
- Number of functions: 1
**Functions:**
```matlab
function HorizRet(saveFlag)
```
---
### conditionmaps.m
**File Statistics:**
- Total lines: 72
- Non-empty lines: 58
- Number of functions: 0
---
### freezeColors.m
**File Statistics:**
- Total lines: 275
- Non-empty lines: 235
- Number of functions: 4
**Functions:**
```matlab
function freezeColors(varargin)
function hout = getCDataHandles(h)
function hAx = getParentAxes(h)
function [h, nancolor] = checkArgs(args)
```
---
### overlaymaps.m
**File Statistics:**
- Total lines: 716
- Non-empty lines: 650
- Number of functions: 1
**Functions:**
```matlab
function overlaymaps(anim,expt)
```
---
### ISIretPlotMaps.m
**File Statistics:**
- Total lines: 673
- Non-empty lines: 580
- Number of functions: 1
**Functions:**
```matlab
function overlaymaps(anim,expt,AltAz)
```
---
### getKmaps.m
**File Statistics:**
- Total lines: 80
- Non-empty lines: 63
- Number of functions: 1
**Functions:**
```matlab
function [kmap] = getKmaps(anim,expt,LP,HP)
```
---
### plotmaps.m
**File Statistics:**
- Total lines: 31
- Non-empty lines: 21
- Number of functions: 0
---
### overlaymaps_new.m
**File Statistics:**
- Total lines: 710
- Non-empty lines: 645
- Number of functions: 1
**Functions:**
```matlab
function overlaymaps_new(anim,expt)
```
---
### VertRet.m
**File Statistics:**
- Total lines: 83
- Non-empty lines: 67
- Number of functions: 1
**Functions:**
```matlab
function VertRet(saveFlag)
```
---
### conditionmapsTF.m
**File Statistics:**
- Total lines: 71
- Non-empty lines: 58
- Number of functions: 0
---
### Retinotopy.m
**File Statistics:**
- Total lines: 335
- Non-empty lines: 299
- Number of functions: 1
**Functions:**
```matlab
function Retinotopy(saveFigsTag, varargin)
```
---
### ShowDiffImage.m
**File Statistics:**
- Total lines: 42
- Non-empty lines: 30
- Number of functions: 0
---
### RetFigures_batch.m
**File Statistics:**
- Total lines: 169
- Non-empty lines: 142
- Number of functions: 1
**Functions:**
```matlab
function RetFigures_batch
```
---
### PlotImage.m
**File Statistics:**
- Total lines: 3
- Non-empty lines: 3
- Number of functions: 0
---
### Script_ISIcontourplots.m
**File Statistics:**
- Total lines: 123
- Non-empty lines: 99
- Number of functions: 0
**File Description:**
Script for analyzing kalatsky retinotopy with 2photon data
---
### overlaymaps_old.m
**File Statistics:**
- Total lines: 627
- Non-empty lines: 528
- Number of functions: 1
**Functions:**
```matlab
function overlaymaps_old(anim,expt,AltAz)
```
---

## Directory: ISIAnGUI/archive
### Gprocessret_old.m
**File Statistics:**
- Total lines: 92
- Non-empty lines: 76
- Number of functions: 1
**Functions:**
```matlab
function [angx magx angy magy] = Gprocessret(f0dum,bw,hh)
```
---
### Gplotretcoverage_old.m
**File Statistics:**
- Total lines: 53
- Non-empty lines: 37
- Number of functions: 1
**Functions:**
```matlab
function Gplotretcoverage(angx,magx,angy,magy)
```
---
### plotpixel_cb_old.m
**File Statistics:**
- Total lines: 132
- Non-empty lines: 106
- Number of functions: 2
**Functions:**
```matlab
function plotpixel_cb
function txt = myupdatefcn(empt,event_obj)
```
---

## Directory: ISIAnGUI/F0
### Gplotcolormap.m
**File Statistics:**
- Total lines: 139
- Non-empty lines: 114
- Number of functions: 2
**Functions:**
```matlab
function Gplotcolormap(mag,ang)
function txt = myupdatefcn(empt,event_obj)
```
---
### BPFkernel.m
**File Statistics:**
- Total lines: 47
- Non-empty lines: 42
- Number of functions: 1
**Functions:**
```matlab
function h = BPFkernel(fhi,flow,HPflag,LPflag,kernel)
```
---
### GprocessOri.m
**File Statistics:**
- Total lines: 50
- Non-empty lines: 40
- Number of functions: 1
**Functions:**
```matlab
function [orimap] = GprocessOri(f0,hh)
```
---
### processEpi.m
**File Statistics:**
- Total lines: 1002
- Non-empty lines: 729
- Number of functions: 72
**Functions:**
```matlab
function varargout = processEpi(varargin)
function processEpi_OpeningFcn(hObject, eventdata, handles, varargin)
function varargout = processEpi_OutputFcn(hObject, eventdata, handles)
function epistart_Callback(hObject, eventdata, handles)
function epistart_CreateFcn(hObject, eventdata, handles)
function epistop_Callback(hObject, eventdata, handles)
function epistop_CreateFcn(hObject, eventdata, handles)
function tau_Callback(hObject, eventdata, handles)
function tau_CreateFcn(hObject, eventdata, handles)
function HPBW_Callback(hObject, eventdata, handles)
function HPBW_CreateFcn(hObject, eventdata, handles)
function LPBW_Callback(hObject, eventdata, handles)
function LPBW_CreateFcn(hObject, eventdata, handles)
function bstart_Callback(hObject, eventdata, handles)
function bstart_CreateFcn(hObject, eventdata, handles)
function bstop_Callback(hObject, eventdata, handles)
function bstop_CreateFcn(hObject, eventdata, handles)
function setimagedir_Callback(hObject, eventdata, handles)
function setimagedir_CreateFcn(hObject, eventdata, handles)
function loadexp_man_Callback(hObject, eventdata, handles)
function loadexp_CreateFcn(hObject, eventdata, handles)
function frameno_Callback(hObject, eventdata, handles)
function frameno_CreateFcn(hObject, eventdata, handles)
function setdirs_Callback(hObject, eventdata, handles)
function loadexp_Callback(hObject, eventdata, handles)
function setdatadir_Callback(hObject, eventdata, handles)
function setdatadir_CreateFcn(hObject, eventdata, handles)
function ROI_Callback(hObject, eventdata, handles)
function process_Callback(hObject, eventdata, handles)
function basesub_Callback(hObject, eventdata, handles)
function tempfilt_Callback(hObject, eventdata, handles)
function episodic_Callback(hObject, eventdata, handles)
function F1_Callback(hObject, eventdata, handles)
function colormap_Callback(hObject, eventdata, handles)
function colormap_CreateFcn(hObject, eventdata, handles)
function setROI_Callback(hObject, eventdata, handles)
function savedata_Callback(hObject, eventdata, handles)
function savefig_Callback(hObject, eventdata, handles)
function refresh_Callback(hObject, eventdata, handles)
function LPflag_Callback(hObject, eventdata, handles)
function HPflag_Callback(hObject, eventdata, handles)
function LPWind_Callback(hObject, eventdata, handles)
function LPWind_CreateFcn(hObject, eventdata, handles)
function HPWind_Callback(hObject, eventdata, handles)
function HPWind_CreateFcn(hObject, eventdata, handles)
function Lpixwidth_Callback(hObject, eventdata, handles)
function Lpixwidth_CreateFcn(hObject, eventdata, handles)
function Hpixwidth_Callback(hObject, eventdata, handles)
function Hpixwidth_CreateFcn(hObject, eventdata, handles)
function processspace_Callback(hObject, eventdata, handles)
function load_Callback(hObject, eventdata, handles)
function pushbutton14_Callback(hObject, eventdata, handles)
function pushbutton15_Callback(hObject, eventdata, handles)
function checkbox1_Callback(hObject, eventdata, handles)
function checkbox2_Callback(hObject, eventdata, handles)
function checkbox3_Callback(hObject, eventdata, handles)
function checkbox4_Callback(hObject, eventdata, handles)
function checkbox5_Callback(hObject, eventdata, handles)
function edit21_Callback(hObject, eventdata, handles)
function edit21_CreateFcn(hObject, eventdata, handles)
function popupmenu6_Callback(hObject, eventdata, handles)
function popupmenu6_CreateFcn(hObject, eventdata, handles)
function edit22_Callback(hObject, eventdata, handles)
function edit22_CreateFcn(hObject, eventdata, handles)
function popupmenu7_Callback(hObject, eventdata, handles)
function popupmenu7_CreateFcn(hObject, eventdata, handles)
function radiobutton9_Callback(hObject, eventdata, handles)
function radiobutton10_Callback(hObject, eventdata, handles)
function pushbutton16_Callback(hObject, eventdata, handles)
function pushbutton17_Callback(hObject, eventdata, handles)
function popupmenu8_Callback(hObject, eventdata, handles)
function popupmenu8_CreateFcn(hObject, eventdata, handles)
```
---
### processF0.m
**File Statistics:**
- Total lines: 1099
- Non-empty lines: 836
- Number of functions: 57
**Functions:**
```matlab
function varargout = processF0(varargin)
function processF0_OpeningFcn(hObject, eventdata, handles, varargin)
function varargout = processF0_OutputFcn(hObject, eventdata, handles)
function process_Callback(hObject, eventdata, handles)
function func_Callback(hObject, eventdata, handles)
function func_CreateFcn(hObject, eventdata, handles)
function load_Callback(hObject, eventdata, handles)
function setimagedir_Callback(hObject, eventdata, handles)
function loadexp_Callback(hObject, eventdata, handles)
function loadexp_CreateFcn(hObject, eventdata, handles)
function setdirs_Callback(hObject, eventdata, handles)
function datadir_Callback(hObject, eventdata, handles)
function datadir_CreateFcn(hObject, eventdata, handles)
function epistart_Callback(hObject, eventdata, handles)
function epistart_CreateFcn(hObject, eventdata, handles)
function epistop_Callback(hObject, eventdata, handles)
function epistop_CreateFcn(hObject, eventdata, handles)
function tau_Callback(hObject, eventdata, handles)
function tau_CreateFcn(hObject, eventdata, handles)
function HPBW_Callback(hObject, eventdata, handles)
function HPBW_CreateFcn(hObject, eventdata, handles)
function LPBW_Callback(hObject, eventdata, handles)
function LPBW_CreateFcn(hObject, eventdata, handles)
function bstart_Callback(hObject, eventdata, handles)
function bstart_CreateFcn(hObject, eventdata, handles)
function bstop_Callback(hObject, eventdata, handles)
function bstop_CreateFcn(hObject, eventdata, handles)
function basesub_Callback(hObject, eventdata, handles)
function tempfilt_Callback(hObject, eventdata, handles)
function Hwidth_Callback(hObject, eventdata, handles)
function Hwidth_CreateFcn(hObject, eventdata, handles)
function HPWind_Callback(hObject, eventdata, handles)
function HPWind_CreateFcn(hObject, eventdata, handles)
function Lwidth_Callback(hObject, eventdata, handles)
function Lwidth_CreateFcn(hObject, eventdata, handles)
function LPWind_Callback(hObject, eventdata, handles)
function LPWind_CreateFcn(hObject, eventdata, handles)
function HPflag_Callback(hObject, eventdata, handles)
function LPflag_Callback(hObject, eventdata, handles)
function setROI_Callback(hObject, eventdata, handles)
function plot_Callback(hObject, eventdata, handles)
function F0im_Callback(hObject, eventdata, handles)
function funcim_Callback(hObject, eventdata, handles)
function retcov_Callback(hObject, eventdata, handles)
function retcont_Callback(hObject, eventdata, handles)
function frameno_Callback(hObject, eventdata, handles)
function frameno_CreateFcn(hObject, eventdata, handles)
function save_Callback(hObject, eventdata, handles)
function trialno_Callback(hObject, eventdata, handles)
function trialno_CreateFcn(hObject, eventdata, handles)
function analyzedir_Callback(hObject, eventdata, handles)
function analyzedir_CreateFcn(hObject, eventdata, handles)
function loadana_Callback(hObject, eventdata, handles)
function loadana_CreateFcn(hObject, eventdata, handles)
function lumFlag_Callback(hObject, eventdata, handles)
function trialVarianceFlag_Callback(hObject, eventdata, handles)
function splitExp_Callback(hObject, eventdata, handles)
```
---
### GprocessColor.m
**File Statistics:**
- Total lines: 67
- Non-empty lines: 56
- Number of functions: 1
**Functions:**
```matlab
function [isolumMap colorSel] = GprocessColor(f0dum,hh)
```
---
### Gplotorimap.m
**File Statistics:**
- Total lines: 208
- Non-empty lines: 199
- Number of functions: 1
**Functions:**
```matlab
function Gplotorimap(mag,ang)
```
---
### GprocessDKL.m
**File Statistics:**
- Total lines: 67
- Non-empty lines: 56
- Number of functions: 1
**Functions:**
```matlab
function [isolumMap colorSel] = GprocessDKL(f0dum,hh)
```
---
### Gplotdirmap.m
**File Statistics:**
- Total lines: 205
- Non-empty lines: 199
- Number of functions: 1
**Functions:**
```matlab
function Gplotorimap(mag,ang)
```
---
### Gplotsfmap.m
**File Statistics:**
- Total lines: 153
- Non-empty lines: 128
- Number of functions: 2
**Functions:**
```matlab
function Gplotsfmap(mag,sf)
function txt = myupdatefcn(empt,event_obj)
```
---
### GprocessDir.m
**File Statistics:**
- Total lines: 49
- Non-empty lines: 39
- Number of functions: 1
**Functions:**
```matlab
function [dirmap] = GprocessDri(f0,hh)
```
---
### Gprocessret.m
**File Statistics:**
- Total lines: 124
- Non-empty lines: 104
- Number of functions: 1
**Functions:**
```matlab
function [angx magx angy magy yrange xrange] = Gprocessret(f0dum,bw,hh)
```
---
### plotpixel_cb.m
**File Statistics:**
- Total lines: 147
- Non-empty lines: 117
- Number of functions: 2
**Functions:**
```matlab
function plotpixel_cb
function txt = myupdatefcn(empt,event_obj)
```
---
### GprocessOcdom.m
**File Statistics:**
- Total lines: 26
- Non-empty lines: 21
- Number of functions: 1
**Functions:**
```matlab
function ocdom = GprocessOcdom(f0dum,bw,hh)
```
---
### condF0_sigma.m
**File Statistics:**
- Total lines: 75
- Non-empty lines: 48
- Number of functions: 1
**Functions:**
```matlab
function [y1 y2] = condF0_sigma(b,normflag,F0_1,F0_2)
```
---
### Gplotretcoverage.m
**File Statistics:**
- Total lines: 64
- Non-empty lines: 46
- Number of functions: 1
**Functions:**
```matlab
function Gplotretcoverage(angx,magx,angy,magy)
```
---
### orimapSplit.m
**File Statistics:**
- Total lines: 10
- Non-empty lines: 8
- Number of functions: 1
**Functions:**
```matlab
function orimapSplit(map1,map2,bw)
```
---
### GprocessSF.m
**File Statistics:**
- Total lines: 48
- Non-empty lines: 41
- Number of functions: 1
**Functions:**
```matlab
function [sfmap mag] = GprocessSF(f0dum,bw,hh)
```
---
### condF0.m
**File Statistics:**
- Total lines: 79
- Non-empty lines: 54
- Number of functions: 1
**Functions:**
```matlab
function [y1 y2 y1_var y2_var] = condF0(Tlim,Tlimb,normflag,varflag)
```
---
### checkSyncs.m
**File Statistics:**
- Total lines: 47
- Non-empty lines: 35
- Number of functions: 1
**Functions:**
```matlab
function [warningflag ddwarningflag] = checkSyncs
```
---
### GprocessColorForm.m
**File Statistics:**
- Total lines: 69
- Non-empty lines: 59
- Number of functions: 1
**Functions:**
```matlab
function [isolumMap colorSel] = GprocessColorForm(f0dum,hh)
```
---

## Directory: ISIAnGUI/F0/New
### getPosSize.m
**File Statistics:**
- Total lines: 38
- Non-empty lines: 29
- Number of functions: 1
**Functions:**
```matlab
function [xpos ypos xsize ysize] = getPosSize
```
---
### plotF0.m
**File Statistics:**
- Total lines: 49
- Non-empty lines: 36
- Number of functions: 1
**Functions:**
```matlab
function plotF0(f0dum,bw,hh)
```
---
### NewF0.m
**File Statistics:**
- Total lines: 957
- Non-empty lines: 717
- Number of functions: 54
**Functions:**
```matlab
function varargout = processF0(varargin)
function processF0_OpeningFcn(hObject, eventdata, handles, varargin)
function varargout = processF0_OutputFcn(hObject, eventdata, handles)
function process_Callback(hObject, eventdata, handles)
function func_Callback(hObject, eventdata, handles)
function func_CreateFcn(hObject, eventdata, handles)
function load_Callback(hObject, eventdata, handles)
function setimagedir_Callback(hObject, eventdata, handles)
function setimagedir_CreateFcn(hObject, eventdata, handles)
function loadexp_Callback(hObject, eventdata, handles)
function loadexp_CreateFcn(hObject, eventdata, handles)
function setdirs_Callback(hObject, eventdata, handles)
function setdatadir_Callback(hObject, eventdata, handles)
function setdatadir_CreateFcn(hObject, eventdata, handles)
function epistart_Callback(hObject, eventdata, handles)
function epistart_CreateFcn(hObject, eventdata, handles)
function epistop_Callback(hObject, eventdata, handles)
function epistop_CreateFcn(hObject, eventdata, handles)
function tau_Callback(hObject, eventdata, handles)
function tau_CreateFcn(hObject, eventdata, handles)
function HPBW_Callback(hObject, eventdata, handles)
function HPBW_CreateFcn(hObject, eventdata, handles)
function LPBW_Callback(hObject, eventdata, handles)
function LPBW_CreateFcn(hObject, eventdata, handles)
function bstart_Callback(hObject, eventdata, handles)
function bstart_CreateFcn(hObject, eventdata, handles)
function bstop_Callback(hObject, eventdata, handles)
function bstop_CreateFcn(hObject, eventdata, handles)
function basesub_Callback(hObject, eventdata, handles)
function tempfilt_Callback(hObject, eventdata, handles)
function Hwidth_Callback(hObject, eventdata, handles)
function Hwidth_CreateFcn(hObject, eventdata, handles)
function HPWind_Callback(hObject, eventdata, handles)
function HPWind_CreateFcn(hObject, eventdata, handles)
function Lwidth_Callback(hObject, eventdata, handles)
function Lwidth_CreateFcn(hObject, eventdata, handles)
function LPWind_Callback(hObject, eventdata, handles)
function LPWind_CreateFcn(hObject, eventdata, handles)
function HPflag_Callback(hObject, eventdata, handles)
function LPflag_Callback(hObject, eventdata, handles)
function setROI_Callback(hObject, eventdata, handles)
function plot_Callback(hObject, eventdata, handles)
function F0im_Callback(hObject, eventdata, handles)
function funcim_Callback(hObject, eventdata, handles)
function retcov_Callback(hObject, eventdata, handles)
function retcont_Callback(hObject, eventdata, handles)
function frameno_Callback(hObject, eventdata, handles)
function frameno_CreateFcn(hObject, eventdata, handles)
function save_Callback(hObject, eventdata, handles)
function pixels_Callback(hObject, eventdata, handles)
function pixels_CreateFcn(hObject, eventdata, handles)
function pixsize_Callback(hObject, eventdata, handles)
function pixsize_CreateFcn(hObject, eventdata, handles)
function pixflag_Callback(hObject, eventdata, handles)
```
---
### Locstd.m
**File Statistics:**
- Total lines: 9
- Non-empty lines: 7
- Number of functions: 1
**Functions:**
```matlab
function out = Locstd(piece)
```
---
### getoridomain.m
**File Statistics:**
- Total lines: 13
- Non-empty lines: 11
- Number of functions: 1
**Functions:**
```matlab
function oridomain = getoridomain
```
---
### reconstructSync.m
**File Statistics:**
- Total lines: 47
- Non-empty lines: 38
- Number of functions: 1
**Functions:**
```matlab
function synctimes = reconstructSync(sync)
```
---
### rc_tdomain.m
**File Statistics:**
- Total lines: 33
- Non-empty lines: 25
- Number of functions: 1
**Functions:**
```matlab
function rc_tdomain(hper,acqT,T)
```
---
### reconstructSync2.m
**File Statistics:**
- Total lines: 49
- Non-empty lines: 39
- Number of functions: 1
**Functions:**
```matlab
function synctimes = reconstructSync2(sync)
```
---

## Directory: ISIAnGUI/F1
### Gf1image.m
**File Statistics:**
- Total lines: 87
- Non-empty lines: 60
- Number of functions: 1
**Functions:**
```matlab
function [y s] = Gf1image(cond,varargin)
```
---
### Gprocesskori.m
**File Statistics:**
- Total lines: 35
- Non-empty lines: 25
- Number of functions: 1
**Functions:**
```matlab
function [kmap delay] = Gprocesskori(f1,bw,hh)
```
---
### adaptiveSmoother.m
**File Statistics:**
- Total lines: 52
- Non-empty lines: 40
- Number of functions: 1
**Functions:**
```matlab
function f = adaptiveSmoother(gcomp,h)
```
---
### Ganticorr.m
**File Statistics:**
- Total lines: 77
- Non-empty lines: 63
- Number of functions: 1
**Functions:**
```matlab
function Ganticorr(f0mdum,bw,hh)
```
---
### Gprocessret.m
**File Statistics:**
- Total lines: 33
- Non-empty lines: 26
- Number of functions: 1
**Functions:**
```matlab
function retmap = Gprocessret(f0dum,bw,hh)
```
---
### Gprocesskret.m
**File Statistics:**
- Total lines: 112
- Non-empty lines: 89
- Number of functions: 1
**Functions:**
```matlab
function [kmap_hor kmap_vert delay_hor delay_vert sh magS] = Gprocesskret(f1,bw,adaptbit,hl,hh)
```
---
### f1image_append.m
**File Statistics:**
- Total lines: 59
- Non-empty lines: 43
- Number of functions: 1
**Functions:**
```matlab
function [y] = f1image_append(cond)
```
---
### GrabContOverlay.m
**File Statistics:**
- Total lines: 58
- Non-empty lines: 38
- Number of functions: 2
**Functions:**
```matlab
function GrabContOverlay(varargin)
function imout = makeplotter(imanat,imfunc,mag,aw,fw,grayid,hsvid)
```
---
### f1image_BPF.m
**File Statistics:**
- Total lines: 79
- Non-empty lines: 57
- Number of functions: 1
**Functions:**
```matlab
function [y] = f1image_BPF(cond)
```
---
### funcAnatomyPlot.m
**File Statistics:**
- Total lines: 60
- Non-empty lines: 42
- Number of functions: 1
**Functions:**
```matlab
function funcAnatomyPlot
```
---
### Groi_scatter.m
**File Statistics:**
- Total lines: 56
- Non-empty lines: 44
- Number of functions: 2
**Functions:**
```matlab
function [R dimv] = Groi_scatter(im1,im2,bw,angflag,oriflag)
function [im1 im2] = circscat(im1,im2);
```
---
### OverlayGuide.m
**File Statistics:**
- Total lines: 336
- Non-empty lines: 254
- Number of functions: 16
**Functions:**
```matlab
function varargout = OverlayGuide(varargin)
function OverlayGuide_OpeningFcn(hObject, eventdata, handles, varargin)
function varargout = OverlayGuide_OutputFcn(hObject, eventdata, handles)
function flipLeftRight_Callback(hObject, eventdata, handles)
function flipUpDown_Callback(hObject, eventdata, handles)
function rotateImage_Callback(hObject, eventdata, handles)
function intensitySlider_Callback(hObject, eventdata, handles)
function intensitySlider_CreateFcn(hObject, eventdata, handles)
function loadImage_Callback(hObject, eventdata, handles)
function plotStatic_Callback(hObject, eventdata, handles)
function grabContOverlay_Callback(hObject, eventdata, handles)
function grabImage_Callback(hObject, eventdata, handles)
function horRet_Callback(hObject, eventdata, handles)
function vertRet_Callback(hObject, eventdata, handles)
function stopGrabbing_Callback(hObject, eventdata, handles)
function sigMag_Callback(hObject, eventdata, handles)
```
---
### processF1.m
**File Statistics:**
- Total lines: 833
- Non-empty lines: 633
- Number of functions: 47
**Functions:**
```matlab
function varargout = processF1(varargin)
function processF1_OpeningFcn(hObject, eventdata, handles, varargin)
function varargout = processF1_OutputFcn(hObject, eventdata, handles)
function process_Callback(hObject, eventdata, handles)
function analyzedir_Callback(hObject, eventdata, handles)
function analyzedir_CreateFcn(hObject, eventdata, handles)
function loadexp_Callback(hObject, eventdata, handles)
function loadexp_CreateFcn(hObject, eventdata, handles)
function setdirs_Callback(hObject, eventdata, handles)
function datadir_Callback(hObject, eventdata, handles)
function datadir_CreateFcn(hObject, eventdata, handles)
function funcim_Callback(hObject, eventdata, handles)
function retcov_Callback(hObject, eventdata, handles)
function retcont_Callback(hObject, eventdata, handles)
function delayim_Callback(hObject, eventdata, handles)
function plot_Callback(hObject, eventdata, handles)
function frameno_Callback(hObject, eventdata, handles)
function frameno_CreateFcn(hObject, eventdata, handles)
function trialno_Callback(hObject, eventdata, handles)
function trialno_CreateFcn(hObject, eventdata, handles)
function setROI_Callback(hObject, eventdata, handles)
function LPWind_Callback(hObject, eventdata, handles)
function LPWind_CreateFcn(hObject, eventdata, handles)
function Lwidth_Callback(hObject, eventdata, handles)
function Lwidth_CreateFcn(hObject, eventdata, handles)
function save_Callback(hObject, eventdata, handles)
function func_Callback(hObject, eventdata, handles)
function func_CreateFcn(hObject, eventdata, handles)
function load_Callback(hObject, eventdata, handles)
function F1im_Callback(hObject, eventdata, handles)
function HPWind_Callback(hObject, eventdata, handles)
function HPWind_CreateFcn(hObject, eventdata, handles)
function HPwidth_Callback(hObject, eventdata, handles)
function HPwidth_CreateFcn(hObject, eventdata, handles)
function HPflag_Callback(hObject, eventdata, handles)
function LPflag_Callback(hObject, eventdata, handles)
function pixels_Callback(hObject, eventdata, handles)
function pixels_CreateFcn(hObject, eventdata, handles)
function pixsize_Callback(hObject, eventdata, handles)
function pixsize_CreateFcn(hObject, eventdata, handles)
function pixflag_Callback(hObject, eventdata, handles)
function edit26_Callback(hObject, eventdata, handles)
function edit26_CreateFcn(hObject, eventdata, handles)
function loadana_Callback(hObject, eventdata, handles)
function loadana_CreateFcn(hObject, eventdata, handles)
function funcAnat_Callback(hObject, eventdata, handles)
function adaptive_Callback(hObject, eventdata, handles)
```
---
### resetImage.m
**File Statistics:**
- Total lines: 40
- Non-empty lines: 28
- Number of functions: 1
**Functions:**
```matlab
function resetImage(trx)
```
---
### Gf1meanimage.m
**File Statistics:**
- Total lines: 52
- Non-empty lines: 39
- Number of functions: 2
**Functions:**
```matlab
function [f1m signals] = Gf1meanimage(varargin)
function y = addtrunc(x,nr)
```
---
### reset_imstate.m
**File Statistics:**
- Total lines: 12
- Non-empty lines: 9
- Number of functions: 1
**Functions:**
```matlab
function reset_imstate
```
---

## Directory: ISI_Processing
### getcondrep.m
**File Statistics:**
- Total lines: 17
- Non-empty lines: 14
- Number of functions: 1
**Functions:**
```matlab
function [cond rep] = getcondrep(ttag)
```
---
### shadow.m
**File Statistics:**
- Total lines: 12
- Non-empty lines: 9
- Number of functions: 1
**Functions:**
```matlab
function sh = shadow(x,y,M,N)
```
---
### getf0im.m
**File Statistics:**
- Total lines: 32
- Non-empty lines: 20
- Number of functions: 1
**Functions:**
```matlab
function f0im = getf0im
```
---
### setAnalyzerDirectory.m
**File Statistics:**
- Total lines: 5
- Non-empty lines: 3
- Number of functions: 1
**Functions:**
```matlab
function setAnalyzerDirectory(path)
```
---
### getframeidx.m
**File Statistics:**
- Total lines: 35
- Non-empty lines: 23
- Number of functions: 1
**Functions:**
```matlab
function Flim = getframeidx(Tlim,varargin)
```
---
### setISIDataDirectory.m
**File Statistics:**
- Total lines: 5
- Non-empty lines: 3
- Number of functions: 1
**Functions:**
```matlab
function setISIDataDirectory(path)
```
---
### loadTrialData.m
**File Statistics:**
- Total lines: 33
- Non-empty lines: 24
- Number of functions: 1
**Functions:**
```matlab
function Tens = loadTrialData(varargin)
```
---
### getTrialFrame.m
**File Statistics:**
- Total lines: 36
- Non-empty lines: 21
- Number of functions: 1
**Functions:**
```matlab
function im = getTrialFrame(fno,varargin)
```
---
### getparam.m
**File Statistics:**
- Total lines: 12
- Non-empty lines: 8
- Number of functions: 1
**Functions:**
```matlab
function pval = getparam(param)
```
---
### gettimetag.m
**File Statistics:**
- Total lines: 5
- Non-empty lines: 3
- Number of functions: 1
**Functions:**
```matlab
function ttag = gettimetag(c,r)
```
---
### getTrialMean.m
**File Statistics:**
- Total lines: 47
- Non-empty lines: 36
- Number of functions: 1
**Functions:**
```matlab
function meanimage = getTrialMean(Tlim,varargin)
```
---
### loadAnalyzer.m
**File Statistics:**
- Total lines: 9
- Non-empty lines: 7
- Number of functions: 1
**Functions:**
```matlab
function loadAnalyzer(ue)
```
---
### plotRetAnat.m
**File Statistics:**
- Total lines: 44
- Non-empty lines: 28
- Number of functions: 0
---
### Fourier_plot.m
**File Statistics:**
- Total lines: 60
- Non-empty lines: 45
- Number of functions: 1
**Functions:**
```matlab
function Fourier_plot(x)
```

---


## Directory: SerenoOverlay

### COSandSerenoOverlay.m

**File Statistics:**
- Total lines: 258
- Non-empty lines: 227
- Number of functions: 1

**Functions:**
```matlab
function COSandSerenoOverlay(anim,AzExpt,AltExpt)
```

---

### generatekmaps.m

**File Statistics:**
- Total lines: 556
- Non-empty lines: 478
- Number of functions: 1

**Functions:**
```matlab
function generatekmaps(anim,expt)
```

---

### generatekret.m

**File Statistics:**
- Total lines: 860
- Non-empty lines: 739
- Number of functions: 1

**Functions:**
```matlab
function generatekret(anim,AzExpt,AltExpt,LP)
```

---

### SerenoAnalysis.m

**File Statistics:**
- Total lines: 171
- Non-empty lines: 146
- Number of functions: 1

**Functions:**
```matlab
function [AreaMap] = SerenoAnalysis(kmap_hor,kmap_vert)
```

---

### Gprocesskret_generatekmaps.m

**File Statistics:**
- Total lines: 93
- Non-empty lines: 75
- Number of functions: 1

**Functions:**
```matlab
function [kmap_hor kmap_vert delay_hor delay_vert magS ang0 ang1 ang2 ang3] = Gprocesskret_generatekmaps(f1,bw,hl,hh)
```

---
