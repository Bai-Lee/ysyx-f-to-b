from evidence import *
from PIL import Image

ON=[0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]
def pixel(img,g,x,y):return img.getpixel((round(g['X']+x*g['WIDTH']/1280),round(g['Y']+y*g['HEIGHT']/960)))[:3]
def led_mask(img,g):
    mask=0
    for i in range(16):
        r,green,b=pixel(img,g,70+(15-i)*30,364)
        if green>180 and r<80 and b<80:mask|=1<<i
    return mask
def digit_mask(img,g,digit):
    ox=63+(7-digit)*46;oy=228
    rects=[(6,3,30,3),(36,6,3,30),(36,39,3,30),(6,69,30,3),(3,39,3,30),(3,6,3,30),(6,36,30,3)]
    value=0
    for i,(x,y,w,h) in enumerate(rects):
        # SDL truncates destination origins and dimensions independently at0.9x.
        px=g['X']+int((ox+x)*g['WIDTH']/1280)+max(1,int(w*g['WIDTH']/1280))//2
        py=g['Y']+int((oy+y)*g['HEIGHT']/960)+max(1,int(h*g['HEIGHT']/960))//2
        r,gr,b=img.getpixel((px,py))[:3]
        if r>180 and gr<80 and b<80:value|=1<<i
    return value
def main():
    d=json.loads((ROOT/'reports/E4_gui.json').read_text('utf8'));results=[];pictures={}
    for r in d['screens']:
        p=ROOT/r['path'];assert sha(p)==r['sha256'];img=Image.open(p).convert('RGB');pictures[r['name']]=img
        assert img.size==(1600,1200)
        if r['name'].startswith('gtkwave_'):continue
        mask=led_mask(img,r['geometry'])
        if r['led_expected'] is not None:assert mask==r['led_expected'],(r['name'],mask,r['led_expected'])
        if r['name']=='official_before':assert mask&255==0
        if r['name']=='official_after_switch':assert mask&255==1
        expected={}
        name=r['name']
        if name.startswith('encoder_'):expected[0]=ON[(r['led_expected']&7)]
        if name.startswith('alu_'):expected[0]=ON[r['led_expected']&15]
        if name in ['lfsr','shift']:expected.update({0:ON[r['led_expected']&15],1:ON[r['led_expected']>>4]})
        if name=='keyboard_a':expected.update(dict(enumerate([ON[12],ON[1],ON[1],ON[6],ON[1],ON[0]])))
        if name=='keyboard_shift_w':expected.update(dict(enumerate([ON[13],ON[1],ON[7],ON[5],ON[2],ON[0]])))
        if name=='keyboard_release':expected.update({i:0 for i in range(4)});expected.update({4:ON[1],5:ON[0]})
        if name=='cpu_sum55':expected.update(dict(enumerate([ON[7],ON[3],ON[7],ON[3]])))
        for i,want in expected.items():assert digit_mask(img,r['geometry'],i)==want,(name,i,digit_mask(img,r['geometry'],i),want)
        if name=='running_light':assert mask and (mask&(mask-1))==0
        if name=='vga_static':
            for y in [100,164,228,356,420]:
                for x in [100,164,228,356,420,548]:
                    rgb=pixel(img,r['geometry'],x,480+y)
                    expected_color=((x%256)&240,(y%256)&240,(((x//8)^(y//8))*17%256)&240)
                    assert rgb==expected_color,(x,y,rgb,expected_color)
        results.append({'name':name,'led_mask':mask,'digits_checked':len(expected),'image_sha256':r['sha256']})
    assert pictures['vga_moving_1'].tobytes()!=pictures['vga_moving_2'].tobytes()
    # Negative control: same actual pixels must not satisfy the wrong LED truth value.
    row=next(r for r in d['screens'] if r['name']=='dual_1');actual=led_mask(pictures['dual_1'],row['geometry']);assert actual==1 and actual!=0
    row=next(r for r in d['screens'] if r['name']=='encoder_270');assert digit_mask(pictures['encoder_270'],row['geometry'],0)!=ON[0]
    dump(ROOT/'reports/E4_visual_check.json',{'status':'PASS','results':results,'negative_control':'The real dual_1 image rejects the false expected LED mask0','vga_pixel_samples':30,'manual_review':'Actual official NVBoard, keyboard ASCII display, VGA test pattern and GTKWave FST traces visually inspected; remaining signals checked from rendered pixels.','scope':'Pixels and physical pin binding in the virtual SDL board; not physical FPGA electrical verification.'})
    d['status']='PASS';dump(ROOT/'reports/E4_gui.json',d)
    print('E4_VISUAL_PASS',len(results),'NVBoard captures;2 GTKWave captures;30 VGA pixel anchors',flush=True)
if __name__=='__main__':main()
