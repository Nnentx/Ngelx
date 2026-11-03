"""Original short gift sound-design effects. Animal/water recordings are separate."""
import math,random,wave,struct,subprocess
from pathlib import Path
out=Path(__file__).resolve().parent/'assets/gifts592';out.mkdir(exist_ok=True)
rate=22050
kinds=['flower','heart','crown','coffee','thumbs_up','tomato','pizza','clock','flame','slipper','pan','plunger','egg','balloon']
for kind in kinds:
    rng=random.Random('ngelx592-'+kind);n=int(rate*(2 if kind=='flame' else .9));samples=[];low=0
    for i in range(n):
        t=i/rate;v=t/(n/rate);noise=rng.uniform(-1,1);low=low*.88+noise*.12
        if kind=='flame':
            x=(low*.8+noise*.14)*(min(1,t*12)*min(1,(2-t)*8))
            if rng.random()<.002:x+=rng.uniform(-.7,.7)
        elif kind in ['tomato','egg','plunger','slipper','balloon']:
            freq={'tomato':95,'egg':900,'plunger':160,'slipper':180,'balloon':60}[kind]
            x=(math.sin(2*math.pi*(freq*t+90*t*t))*.45+noise*.5)*math.exp(-t*(14 if kind=='balloon' else 7))
            if kind=='tomato':x+=low*.5*math.exp(-t*3)
        elif kind=='pan':
            x=sum(math.sin(2*math.pi*f*t)*a for f,a in [(650,.25),(1037,.2),(1790,.15)])*math.exp(-t*5)
        elif kind=='clock':
            x=noise*.5*math.exp(-(t%0.2)*80)+math.sin(2*math.pi*1500*t)*.08*math.exp(-t*3)
        elif kind=='pizza':
            x=(noise-low)*.45*math.sin(math.pi*v)**2
        elif kind=='coffee':
            x=low*.6*math.sin(math.pi*v)+math.sin(2*math.pi*(700*t+400*t*t))*.15*math.exp(-t*4)
        else:
            root={'flower':880,'heart':660,'crown':1047,'thumbs_up':784}[kind]
            x=sum(math.sin(2*math.pi*root*factor*t)*amp for factor,amp in [(1,.25),(1.5,.12),(2,.06)])*math.exp(-t*4)
        samples.append(max(-.9,min(.9,x))*min(1,t/.008))
    peak=max(map(abs,samples)) or 1
    wav=out/(kind+'.wav')
    with wave.open(str(wav),'wb') as f:
        f.setparams((1,2,rate,0,'NONE','not compressed'));f.writeframes(b''.join(struct.pack('<h',int(x/peak*.7*32767)) for x in samples))
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(wav),'-b:a','96k',str(out/(kind+'.mp3'))],check=True)
    wav.unlink()
