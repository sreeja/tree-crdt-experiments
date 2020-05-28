curl "http://localhost:6001/move?n=aaa&p=aa&np=ab" & curl "http://localhost:6002/move?n=ab&p=a&np=aaa" & curl "http://localhost:6003/move?n=cfd&p=cf&np=c"
wait 
curl "http://localhost:6001/move?n=aba&p=ab&np=ac" & curl "http://localhost:6002/move?n=ac&p=a&np=aba" & curl "http://localhost:6003/move?n=cfd&p=c&np=cf"
wait 
curl "http://localhost:6001/move?n=aca&p=ac&np=ad" & curl "http://localhost:6002/move?n=ad&p=a&np=aca" & curl "http://localhost:6003/move?n=cff&p=cf&np=c"
wait 
curl "http://localhost:6001/move?n=afd&p=af&np=a" & curl "http://localhost:6002/move?n=baa&p=ba&np=bb" & curl "http://localhost:6003/move?n=bb&p=b&np=baa"
wait 
curl "http://localhost:6001/move?n=afd&p=a&np=af" & curl "http://localhost:6002/move?n=bba&p=bb&np=bc" & curl "http://localhost:6003/move?n=bc&p=b&np=bba"
wait 
curl "http://localhost:6001/move?n=afb&p=af&np=a" & curl "http://localhost:6002/move?n=bca&p=bc&np=bd" & curl "http://localhost:6003/move?n=bd&p=b&np=bca"
wait 
curl "http://localhost:6001/move?n=cb&p=c&np=caa" & curl "http://localhost:6002/move?n=bfc&p=bf&np=b" & curl "http://localhost:6003/move?n=caa&p=ca&np=cb"
wait 
curl "http://localhost:6001/move?n=cc&p=c&np=cba" & curl "http://localhost:6002/move?n=bfc&p=b&np=bf" & curl "http://localhost:6003/move?n=cba&p=cb&np=cc"
wait 
curl "http://localhost:6001/move?n=cd&p=c&np=cca" & curl "http://localhost:6002/move?n=bff&p=bf&np=b" & curl "http://localhost:6003/move?n=cca&p=cc&np=cd"
wait 
curl "http://localhost:6001/move?n=afb&p=a&np=af" & curl "http://localhost:6002/move?n=bff&p=b&np=bf" & curl "http://localhost:6003/move?n=cff&p=c&np=cf"
wait 
curl "http://localhost:6001/move?n=afe&p=af&np=a" & curl "http://localhost:6002/move?n=bfd&p=bf&np=b" & curl "http://localhost:6003/move?n=cff&p=cf&np=c"
wait 
curl "http://localhost:6001/move?n=afe&p=a&np=af" & curl "http://localhost:6002/move?n=bfd&p=b&np=bf" & curl "http://localhost:6003/move?n=cff&p=c&np=cf"
wait 
curl "http://localhost:6001/move?n=afb&p=af&np=a" & curl "http://localhost:6002/move?n=bfd&p=bf&np=b" & curl "http://localhost:6003/move?n=cfb&p=cf&np=c"
wait 
curl "http://localhost:6001/move?n=afb&p=a&np=af" & curl "http://localhost:6002/move?n=bfd&p=b&np=bf" & curl "http://localhost:6003/move?n=cfb&p=c&np=cf"
wait 
curl "http://localhost:6001/add?n=cac01&p=cac" & curl "http://localhost:6002/add?n=ab02&p=ab" & curl "http://localhost:6003/add?n=c03&p=c"
wait 
curl "http://localhost:6001/remove?n=cac01&p=cac" & curl "http://localhost:6002/remove?n=ab02&p=ab" & curl "http://localhost:6003/remove?n=c03&p=c"
wait 
curl "http://localhost:6001/add?n=aa11&p=aa" & curl "http://localhost:6002/add?n=ac12&p=ac" & curl "http://localhost:6003/add?n=bca13&p=bca"
wait 
curl "http://localhost:6001/add?n=cb21&p=cb" & curl "http://localhost:6002/add?n=acc22&p=acc" & curl "http://localhost:6003/add?n=aab23&p=aab"
wait 
curl "http://localhost:6001/add?n=cb31&p=cb" & curl "http://localhost:6002/add?n=bb32&p=bb" & curl "http://localhost:6003/add?n=b33&p=b"
wait 
curl "http://localhost:6001/add?n=ccb41&p=ccb" & curl "http://localhost:6002/add?n=ac42&p=ac" & curl "http://localhost:6003/add?n=b43&p=b"
wait 
curl "http://localhost:6001/add?n=ab51&p=ab" & curl "http://localhost:6002/add?n=ac52&p=ac" & curl "http://localhost:6003/add?n=ca53&p=ca"
wait 
curl "http://localhost:6001/remove?n=ab51&p=ab" & curl "http://localhost:6002/remove?n=ac52&p=ac" & curl "http://localhost:6003/remove?n=ca53&p=ca"
wait 
curl "http://localhost:6001/add?n=cbb61&p=cbb" & curl "http://localhost:6002/add?n=ac62&p=ac" & curl "http://localhost:6003/add?n=ccc63&p=ccc"
wait 
curl "http://localhost:6001/add?n=abc71&p=abc" & curl "http://localhost:6002/add?n=aca72&p=aca" & curl "http://localhost:6003/add?n=baa73&p=baa"
wait 
curl "http://localhost:6001/add?n=aca81&p=aca" & curl "http://localhost:6002/add?n=acb82&p=acb" & curl "http://localhost:6003/add?n=bc83&p=bc"
wait 
curl "http://localhost:6001/add?n=cbb91&p=cbb" & curl "http://localhost:6002/add?n=bbb92&p=bbb" & curl "http://localhost:6003/add?n=cca93&p=cca"
wait 
curl "http://localhost:6001/add?n=aac101&p=aac" & curl "http://localhost:6002/add?n=ac102&p=ac" & curl "http://localhost:6003/add?n=bc103&p=bc"
wait 
curl "http://localhost:6001/remove?n=aac101&p=aac" & curl "http://localhost:6002/remove?n=ac102&p=ac" & curl "http://localhost:6003/remove?n=bc103&p=bc"
wait 
curl "http://localhost:6001/add?n=aa111&p=aa" & curl "http://localhost:6002/add?n=aaa112&p=aaa" & curl "http://localhost:6003/add?n=cca113&p=cca"
wait 
curl "http://localhost:6001/add?n=cb121&p=cb" & curl "http://localhost:6002/add?n=aa122&p=aa" & curl "http://localhost:6003/add?n=bcc123&p=bcc"
wait 
curl "http://localhost:6001/add?n=bbc131&p=bbc" & curl "http://localhost:6002/add?n=bba132&p=bba" & curl "http://localhost:6003/add?n=a133&p=a"
wait 
curl "http://localhost:6001/add?n=cac141&p=cac" & curl "http://localhost:6002/add?n=bac142&p=bac" & curl "http://localhost:6003/add?n=caa143&p=caa"
wait 
curl "http://localhost:6001/add?n=bcb151&p=bcb" & curl "http://localhost:6002/add?n=b152&p=b" & curl "http://localhost:6003/add?n=bac153&p=bac"
wait 
curl "http://localhost:6001/remove?n=bcb151&p=bcb" & curl "http://localhost:6002/remove?n=b152&p=b" & curl "http://localhost:6003/remove?n=bac153&p=bac"
wait 
curl "http://localhost:6001/add?n=ca161&p=ca" & curl "http://localhost:6002/add?n=aa162&p=aa" & curl "http://localhost:6003/add?n=caa163&p=caa"
wait 
curl "http://localhost:6001/add?n=cb171&p=cb" & curl "http://localhost:6002/add?n=bba172&p=bba" & curl "http://localhost:6003/add?n=bab173&p=bab"
wait 
curl "http://localhost:6001/add?n=aa181&p=aa" & curl "http://localhost:6002/add?n=cbc182&p=cbc" & curl "http://localhost:6003/add?n=cab183&p=cab"
wait 
curl "http://localhost:6001/add?n=ac191&p=ac" & curl "http://localhost:6002/add?n=cb192&p=cb" & curl "http://localhost:6003/add?n=bcb193&p=bcb"
wait 
curl "http://localhost:6001/add?n=ac201&p=ac" & curl "http://localhost:6002/add?n=bbc202&p=bbc" & curl "http://localhost:6003/add?n=ac203&p=ac"
wait 
curl "http://localhost:6001/remove?n=ac201&p=ac" & curl "http://localhost:6002/remove?n=bbc202&p=bbc" & curl "http://localhost:6003/remove?n=ac203&p=ac"
wait 
curl "http://localhost:6001/add?n=bcb211&p=bcb" & curl "http://localhost:6002/add?n=bb212&p=bb" & curl "http://localhost:6003/add?n=acc213&p=acc"
wait 
curl "http://localhost:6001/add?n=a221&p=a" & curl "http://localhost:6002/add?n=ba222&p=ba" & curl "http://localhost:6003/add?n=a223&p=a"
wait 
curl "http://localhost:6001/add?n=abc231&p=abc" & curl "http://localhost:6002/add?n=aa232&p=aa" & curl "http://localhost:6003/add?n=ab233&p=ab"
wait 
curl "http://localhost:6001/add?n=bc241&p=bc" & curl "http://localhost:6002/add?n=bba242&p=bba" & curl "http://localhost:6003/add?n=cab243&p=cab"
wait 
curl "http://localhost:6001/add?n=aa251&p=aa" & curl "http://localhost:6002/add?n=aca252&p=aca" & curl "http://localhost:6003/add?n=bc253&p=bc"
wait 
curl "http://localhost:6001/remove?n=aa251&p=aa" & curl "http://localhost:6002/remove?n=aca252&p=aca" & curl "http://localhost:6003/remove?n=bc253&p=bc"
wait 
curl "http://localhost:6001/add?n=c261&p=c" & curl "http://localhost:6002/add?n=cca262&p=cca" & curl "http://localhost:6003/add?n=aa263&p=aa"
wait 
curl "http://localhost:6001/add?n=bc271&p=bc" & curl "http://localhost:6002/add?n=cb272&p=cb" & curl "http://localhost:6003/add?n=acc273&p=acc"
wait 
curl "http://localhost:6001/add?n=cca281&p=cca" & curl "http://localhost:6002/add?n=ccc282&p=ccc" & curl "http://localhost:6003/add?n=ca283&p=ca"
wait 
curl "http://localhost:6001/add?n=bba291&p=bba" & curl "http://localhost:6002/add?n=aa292&p=aa" & curl "http://localhost:6003/add?n=aba293&p=aba"
wait 
