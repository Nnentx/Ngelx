import {readFileSync,writeFileSync} from 'node:fs';
const source=new URL('../../server/verification561/',import.meta.url);
const image=readFileSync(new URL('verification-envelope.png',source)).toString('base64');
const template=readFileSync(new URL('template.mjs',source),'utf8').replace("import {readFileSync} from 'node:fs';",'// Generated approved template.').replace("readFileSync(new URL('./verification-envelope.png',import.meta.url)).toString('base64')",JSON.stringify(image));
writeFileSync(new URL('./template.generated.mjs',import.meta.url),template);
writeFileSync(new URL('./handler.generated.mjs',import.meta.url),readFileSync(new URL('handler.mjs',source),'utf8').replace("'./template.mjs'","'./template.generated.mjs'"));
