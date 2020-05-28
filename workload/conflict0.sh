curl "http://localhost:6001/move?n=aea&p=ae&np=a" & curl "http://localhost:6002/move?n=bea&p=be&np=b" & curl "http://localhost:6003/move?n=cea&p=ce&np=c"
wait 
curl "http://localhost:6001/move?n=aea&p=a&np=ae" & curl "http://localhost:6002/move?n=bea&p=b&np=be" & curl "http://localhost:6003/move?n=cea&p=c&np=ce"
wait 
curl "http://localhost:6001/move?n=aff&p=af&np=a" & curl "http://localhost:6002/move?n=bff&p=bf&np=b" & curl "http://localhost:6003/move?n=cff&p=cf&np=c"
wait 
curl "http://localhost:6001/move?n=aff&p=a&np=af" & curl "http://localhost:6002/move?n=bff&p=b&np=bf" & curl "http://localhost:6003/move?n=cff&p=c&np=cf"
wait 
curl "http://localhost:6001/move?n=agc&p=ag&np=a" & curl "http://localhost:6002/move?n=bgc&p=bg&np=b" & curl "http://localhost:6003/move?n=cgc&p=cg&np=c"
wait 
curl "http://localhost:6001/move?n=agc&p=a&np=ag" & curl "http://localhost:6002/move?n=bgc&p=b&np=bg" & curl "http://localhost:6003/move?n=cgc&p=c&np=cg"
wait 
curl "http://localhost:6001/move?n=acg&p=ac&np=a" & curl "http://localhost:6002/move?n=bcg&p=bc&np=b" & curl "http://localhost:6003/move?n=ccg&p=cc&np=c"
wait 
curl "http://localhost:6001/move?n=acg&p=a&np=ac" & curl "http://localhost:6002/move?n=bcg&p=b&np=bc" & curl "http://localhost:6003/move?n=ccg&p=c&np=cc"
wait 
curl "http://localhost:6001/move?n=aac&p=aa&np=a" & curl "http://localhost:6002/move?n=bac&p=ba&np=b" & curl "http://localhost:6003/move?n=cac&p=ca&np=c"
wait 
curl "http://localhost:6001/move?n=aac&p=a&np=aa" & curl "http://localhost:6002/move?n=bac&p=b&np=ba" & curl "http://localhost:6003/move?n=cac&p=c&np=ca"
wait 
curl "http://localhost:6001/move?n=abe&p=ab&np=a" & curl "http://localhost:6002/move?n=bbe&p=bb&np=b" & curl "http://localhost:6003/move?n=cbe&p=cb&np=c"
wait 
curl "http://localhost:6001/move?n=abe&p=a&np=ab" & curl "http://localhost:6002/move?n=bbe&p=b&np=bb" & curl "http://localhost:6003/move?n=cbe&p=c&np=cb"
wait 
curl "http://localhost:6001/move?n=abc&p=ab&np=a" & curl "http://localhost:6002/move?n=bbc&p=bb&np=b" & curl "http://localhost:6003/move?n=cbc&p=cb&np=c"
wait 
curl "http://localhost:6001/move?n=abc&p=a&np=ab" & curl "http://localhost:6002/move?n=bbc&p=b&np=bb" & curl "http://localhost:6003/move?n=cbc&p=c&np=cb"
wait 
curl "http://localhost:6001/add?n=bc01&p=bc" & curl "http://localhost:6002/add?n=cbb02&p=cbb" & curl "http://localhost:6003/add?n=aab03&p=aab"
wait 
curl "http://localhost:6001/remove?n=bc01&p=bc" & curl "http://localhost:6002/remove?n=cbb02&p=cbb" & curl "http://localhost:6003/remove?n=aab03&p=aab"
wait 
curl "http://localhost:6001/add?n=cc11&p=cc" & curl "http://localhost:6002/add?n=c12&p=c" & curl "http://localhost:6003/add?n=aa13&p=aa"
wait 
curl "http://localhost:6001/add?n=ba21&p=ba" & curl "http://localhost:6002/add?n=ca22&p=ca" & curl "http://localhost:6003/add?n=bc23&p=bc"
wait 
curl "http://localhost:6001/add?n=caa31&p=caa" & curl "http://localhost:6002/add?n=ab32&p=ab" & curl "http://localhost:6003/add?n=ac33&p=ac"
wait 
curl "http://localhost:6001/add?n=ab41&p=ab" & curl "http://localhost:6002/add?n=bbb42&p=bbb" & curl "http://localhost:6003/add?n=bba43&p=bba"
wait 
curl "http://localhost:6001/add?n=cca51&p=cca" & curl "http://localhost:6002/add?n=ca52&p=ca" & curl "http://localhost:6003/add?n=bca53&p=bca"
wait 
curl "http://localhost:6001/remove?n=cca51&p=cca" & curl "http://localhost:6002/remove?n=ca52&p=ca" & curl "http://localhost:6003/remove?n=bca53&p=bca"
wait 
curl "http://localhost:6001/add?n=aab61&p=aab" & curl "http://localhost:6002/add?n=bb62&p=bb" & curl "http://localhost:6003/add?n=cbb63&p=cbb"
wait 
curl "http://localhost:6001/add?n=ccc71&p=ccc" & curl "http://localhost:6002/add?n=bb72&p=bb" & curl "http://localhost:6003/add?n=ba73&p=ba"
wait 
curl "http://localhost:6001/add?n=bb81&p=bb" & curl "http://localhost:6002/add?n=cba82&p=cba" & curl "http://localhost:6003/add?n=bb83&p=bb"
wait 
curl "http://localhost:6001/add?n=abb91&p=abb" & curl "http://localhost:6002/add?n=aab92&p=aab" & curl "http://localhost:6003/add?n=aba93&p=aba"
wait 
curl "http://localhost:6001/add?n=cac101&p=cac" & curl "http://localhost:6002/add?n=abc102&p=abc" & curl "http://localhost:6003/add?n=aa103&p=aa"
wait 
curl "http://localhost:6001/remove?n=cac101&p=cac" & curl "http://localhost:6002/remove?n=abc102&p=abc" & curl "http://localhost:6003/remove?n=aa103&p=aa"
wait 
curl "http://localhost:6001/add?n=cac111&p=cac" & curl "http://localhost:6002/add?n=aab112&p=aab" & curl "http://localhost:6003/add?n=caa113&p=caa"
wait 
curl "http://localhost:6001/add?n=ccc121&p=ccc" & curl "http://localhost:6002/add?n=abc122&p=abc" & curl "http://localhost:6003/add?n=ca123&p=ca"
wait 
curl "http://localhost:6001/add?n=ac131&p=ac" & curl "http://localhost:6002/add?n=bcc132&p=bcc" & curl "http://localhost:6003/add?n=bab133&p=bab"
wait 
curl "http://localhost:6001/add?n=bcb141&p=bcb" & curl "http://localhost:6002/add?n=cc142&p=cc" & curl "http://localhost:6003/add?n=bcc143&p=bcc"
wait 
curl "http://localhost:6001/add?n=a151&p=a" & curl "http://localhost:6002/add?n=bc152&p=bc" & curl "http://localhost:6003/add?n=abc153&p=abc"
wait 
curl "http://localhost:6001/remove?n=a151&p=a" & curl "http://localhost:6002/remove?n=bc152&p=bc" & curl "http://localhost:6003/remove?n=abc153&p=abc"
wait 
curl "http://localhost:6001/add?n=abc161&p=abc" & curl "http://localhost:6002/add?n=aa162&p=aa" & curl "http://localhost:6003/add?n=ccc163&p=ccc"
wait 
curl "http://localhost:6001/add?n=bab171&p=bab" & curl "http://localhost:6002/add?n=bbb172&p=bbb" & curl "http://localhost:6003/add?n=cc173&p=cc"
wait 
curl "http://localhost:6001/add?n=aab181&p=aab" & curl "http://localhost:6002/add?n=cbc182&p=cbc" & curl "http://localhost:6003/add?n=ac183&p=ac"
wait 
curl "http://localhost:6001/add?n=bba191&p=bba" & curl "http://localhost:6002/add?n=aa192&p=aa" & curl "http://localhost:6003/add?n=ba193&p=ba"
wait 
curl "http://localhost:6001/add?n=cac201&p=cac" & curl "http://localhost:6002/add?n=aba202&p=aba" & curl "http://localhost:6003/add?n=abb203&p=abb"
wait 
curl "http://localhost:6001/remove?n=cac201&p=cac" & curl "http://localhost:6002/remove?n=aba202&p=aba" & curl "http://localhost:6003/remove?n=abb203&p=abb"
wait 
curl "http://localhost:6001/add?n=acc211&p=acc" & curl "http://localhost:6002/add?n=c212&p=c" & curl "http://localhost:6003/add?n=cba213&p=cba"
wait 
curl "http://localhost:6001/add?n=ab221&p=ab" & curl "http://localhost:6002/add?n=bba222&p=bba" & curl "http://localhost:6003/add?n=bbc223&p=bbc"
wait 
curl "http://localhost:6001/add?n=ac231&p=ac" & curl "http://localhost:6002/add?n=bcc232&p=bcc" & curl "http://localhost:6003/add?n=cc233&p=cc"
wait 
curl "http://localhost:6001/add?n=ccc241&p=ccc" & curl "http://localhost:6002/add?n=cba242&p=cba" & curl "http://localhost:6003/add?n=acb243&p=acb"
wait 
curl "http://localhost:6001/add?n=bca251&p=bca" & curl "http://localhost:6002/add?n=cbc252&p=cbc" & curl "http://localhost:6003/add?n=cc253&p=cc"
wait 
curl "http://localhost:6001/remove?n=bca251&p=bca" & curl "http://localhost:6002/remove?n=cbc252&p=cbc" & curl "http://localhost:6003/remove?n=cc253&p=cc"
wait 
curl "http://localhost:6001/add?n=cca261&p=cca" & curl "http://localhost:6002/add?n=bbc262&p=bbc" & curl "http://localhost:6003/add?n=bbb263&p=bbb"
wait 
curl "http://localhost:6001/add?n=ba271&p=ba" & curl "http://localhost:6002/add?n=cc272&p=cc" & curl "http://localhost:6003/add?n=ab273&p=ab"
wait 
curl "http://localhost:6001/add?n=bb281&p=bb" & curl "http://localhost:6002/add?n=cb282&p=cb" & curl "http://localhost:6003/add?n=cbc283&p=cbc"
wait 
curl "http://localhost:6001/add?n=aca291&p=aca" & curl "http://localhost:6002/add?n=bb292&p=bb" & curl "http://localhost:6003/add?n=bba293&p=bba"
wait 
