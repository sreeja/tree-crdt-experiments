curl "http://localhost:6001/upmove?n=aaa&p=aa&np=ab&ca=ab" & curl "http://localhost:6002/downmove?n=ab&p=a&np=aaa&ca=aaa,aa" & curl "http://localhost:6003/upmove?n=cea&p=ce&np=c"
wait 
curl "http://localhost:6001/downmove?n=aea&p=ae&np=aeb&ca=aeb" & curl "http://localhost:6002/upmove?n=baa&p=ba&np=bb&ca=bb" & curl "http://localhost:6003/downmove?n=bb&p=b&np=baa&ca=baa,ba"
wait 
curl "http://localhost:6001/upmove?n=aff&p=af&np=a" & curl "http://localhost:6002/upmove?n=bff&p=bf&np=b" & curl "http://localhost:6003/upmove?n=cff&p=cf&np=c"
wait 
curl "http://localhost:6001/downmove?n=aff&p=a&np=af&ca=af" & curl "http://localhost:6002/downmove?n=bff&p=b&np=bf&ca=bf" & curl "http://localhost:6003/downmove?n=cff&p=c&np=cf&ca=cf"
wait 
curl "http://localhost:6001/upmove?n=agc&p=ag&np=a" & curl "http://localhost:6002/upmove?n=bgc&p=bg&np=b" & curl "http://localhost:6003/upmove?n=cgc&p=cg&np=c"
wait 
curl "http://localhost:6001/downmove?n=agc&p=a&np=ag&ca=ag" & curl "http://localhost:6002/downmove?n=bgc&p=b&np=bg&ca=bg" & curl "http://localhost:6003/downmove?n=cgc&p=c&np=cg&ca=cg"
wait 
curl "http://localhost:6001/upmove?n=acg&p=ac&np=a" & curl "http://localhost:6002/upmove?n=bcg&p=bc&np=b" & curl "http://localhost:6003/upmove?n=ccg&p=cc&np=c"
wait 
curl "http://localhost:6001/downmove?n=acg&p=a&np=ac&ca=ac" & curl "http://localhost:6002/downmove?n=bcg&p=b&np=bc&ca=bc" & curl "http://localhost:6003/downmove?n=ccg&p=c&np=cc&ca=cc"
wait 
curl "http://localhost:6001/upmove?n=aac&p=aa&np=a" & curl "http://localhost:6002/upmove?n=bac&p=ba&np=b" & curl "http://localhost:6003/upmove?n=cac&p=ca&np=c"
wait 
curl "http://localhost:6001/downmove?n=aac&p=a&np=aa&ca=aa" & curl "http://localhost:6002/downmove?n=bac&p=b&np=ba&ca=ba" & curl "http://localhost:6003/downmove?n=cac&p=c&np=ca&ca=ca"
wait 
curl "http://localhost:6001/upmove?n=abe&p=ab&np=a" & curl "http://localhost:6002/upmove?n=bbe&p=bb&np=b" & curl "http://localhost:6003/upmove?n=cbe&p=cb&np=c"
wait 
curl "http://localhost:6001/downmove?n=abe&p=a&np=ab&ca=ab" & curl "http://localhost:6002/downmove?n=bbe&p=b&np=bb&ca=bb" & curl "http://localhost:6003/downmove?n=cbe&p=c&np=cb&ca=cb"
wait 
curl "http://localhost:6001/upmove?n=abc&p=ab&np=a" & curl "http://localhost:6002/upmove?n=bbc&p=bb&np=b" & curl "http://localhost:6003/upmove?n=cbc&p=cb&np=c"
wait 
curl "http://localhost:6001/downmove?n=abc&p=a&np=ab&ca=ab" & curl "http://localhost:6002/downmove?n=bbc&p=b&np=bb&ca=bb" & curl "http://localhost:6003/downmove?n=cbc&p=c&np=cb&ca=cb"
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
