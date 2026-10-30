from common7 import *
import re,gzip,collections
def main():
 pdk=Path('/home/USER/tools/icsprout55-e-stage');areas={};geometry={}
 for vt in ['R','L']:
  root=pdk/('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7C'+vt)
  text=(root/'liberty'/('ics55_LLSC_H7C'+vt+'_typ_tt_1p2_25_nldm.lib')).read_text()
  pieces=re.split(r'\bcell\s*\(\s*"?([^\s\)\"]+)"?\s*\)\s*\{',text)
  for i in range(1,len(pieces),2):
   match=re.search(r'\barea\s*:\s*([\d.eE+-]+)',pieces[i+1]);assert match,pieces[i];areas[pieces[i]]=float(match[1])
  lef=(root/'lef'/('ics55_LLSC_H7C'+vt+'_ecos.lef')).read_text()
  for name,body in re.findall(r'^MACRO\s+(\S+)\s*\n(.*?)^END\s+\1\s*$',lef,re.M|re.S):
   size=re.search(r'\bSIZE\s+([\d.]+)\s+BY\s+([\d.]+)',body);assert size;geometry[name]=float(size[1])*float(size[2])
 rows=[]
 for variant in json.loads((ROOT/'reports/E7_synthesis.json').read_text())['variants']:
  net=ROOT/'E/E7/synthesis'/variant['variant']/'e7_minirv_Synthesis.v.gz';text=gzip.decompress(net.read_bytes()).decode();counts=collections.Counter()
  for kind,inst,body in re.findall(r'\b(\w+)\s+(\\\S+|\w+)\s*\((.*?)\);',text,re.S):
   if kind in areas:counts[kind]+=1
  assert sum(counts.values())==variant['mapped_instances']
  lib=sum(areas[c]*n for c,n in counts.items());lef=sum(geometry[c]*n for c,n in counts.items());reported=variant['cell_area_um2']
  assert abs(lib-reported)<2 and abs(lib-lef)<max(.01,lib*.001),(variant['variant'],lib,lef,reported)
  rows.append({'variant':variant['variant'],'instances':sum(counts.values()),'liberty_area_sum':lib,'lef_geometry_sum_um2':lef,'reported_rounded_area_um2':reported,'cell_counts':dict(counts)})
 dump(ROOT/'reports/E7_area_units.json',{'status':'PASS','variants':rows,'meaning':'Independent sum of actual mappedcellLibertyareas agreeswithLEFSIZE(width*height)inmicrons androundedSTAarea. This grounds the unit conversion used by the hypotheticalcostexercise.'})
 print('STANDARD_CELL_AREA_UNITS_AND_COUNTS_VERIFIED',flush=True)
if __name__=='__main__':main()
