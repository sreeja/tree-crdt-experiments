curl "http://localhost:6001/move?n=aaa&p=aa&np=ab" & curl "http://localhost:6002/move?n=ab&p=a&np=aaa" & curl "http://localhost:6003/move?n=cge&p=cg&np=c"
wait 
curl "http://localhost:6001/move?n=aba&p=ab&np=ac" & curl "http://localhost:6002/move?n=ac&p=a&np=aba" & curl "http://localhost:6003/move?n=cge&p=c&np=cg"
wait 
curl "http://localhost:6001/move?n=aca&p=ac&np=ad" & curl "http://localhost:6002/move?n=ad&p=a&np=aca" & curl "http://localhost:6003/move?n=cge&p=cg&np=c"
wait 
curl "http://localhost:6001/move?n=ada&p=ad&np=ae" & curl "http://localhost:6002/move?n=ae&p=a&np=ada" & curl "http://localhost:6003/move?n=cge&p=c&np=cg"
wait 
curl "http://localhost:6001/move?n=aea&p=ae&np=af" & curl "http://localhost:6002/move?n=af&p=a&np=aea" & curl "http://localhost:6003/add?n=aa03&p=aa"
wait 
curl "http://localhost:6001/move?n=agc&p=ag&np=a" & curl "http://localhost:6002/move?n=baa&p=ba&np=bb" & curl "http://localhost:6003/move?n=bb&p=b&np=baa"
wait 
curl "http://localhost:6001/move?n=agc&p=a&np=ag" & curl "http://localhost:6002/move?n=bba&p=bb&np=bc" & curl "http://localhost:6003/move?n=bc&p=b&np=bba"
wait 
curl "http://localhost:6001/move?n=aga&p=ag&np=a" & curl "http://localhost:6002/move?n=bca&p=bc&np=bd" & curl "http://localhost:6003/move?n=bd&p=b&np=bca"
wait 
curl "http://localhost:6001/move?n=aga&p=a&np=ag" & curl "http://localhost:6002/move?n=bda&p=bd&np=be" & curl "http://localhost:6003/move?n=be&p=b&np=bda"
wait 
curl "http://localhost:6001/add?n=aa01&p=aa" & curl "http://localhost:6002/move?n=bea&p=be&np=bf" & curl "http://localhost:6003/move?n=bf&p=b&np=bea"
wait 
curl "http://localhost:6001/move?n=cb&p=c&np=caa" & curl "http://localhost:6002/move?n=bgg&p=bg&np=b" & curl "http://localhost:6003/move?n=caa&p=ca&np=cb"
wait 
curl "http://localhost:6001/move?n=cc&p=c&np=cba" & curl "http://localhost:6002/move?n=bgg&p=b&np=bg" & curl "http://localhost:6003/move?n=cba&p=cb&np=cc"
wait 
curl "http://localhost:6001/move?n=cd&p=c&np=cca" & curl "http://localhost:6002/move?n=bga&p=bg&np=b" & curl "http://localhost:6003/move?n=cca&p=cc&np=cd"
wait 
curl "http://localhost:6001/move?n=ce&p=c&np=cda" & curl "http://localhost:6002/move?n=bga&p=b&np=bg" & curl "http://localhost:6003/move?n=cda&p=cd&np=ce"
wait 
curl "http://localhost:6001/move?n=cf&p=c&np=cea" & curl "http://localhost:6002/add?n=bb02&p=bb" & curl "http://localhost:6003/move?n=cea&p=ce&np=cf"
wait 
curl "http://localhost:6001/remove?n=aa01&p=aa" & curl "http://localhost:6002/remove?n=bb02&p=bb" & curl "http://localhost:6003/remove?n=aa03&p=aa"
wait 
curl "http://localhost:6001/add?n=bc11&p=bc" & curl "http://localhost:6002/add?n=aaa12&p=aaa" & curl "http://localhost:6003/add?n=aa13&p=aa"
wait 
curl "http://localhost:6001/add?n=baa21&p=baa" & curl "http://localhost:6002/add?n=bcb22&p=bcb" & curl "http://localhost:6003/add?n=cb23&p=cb"
wait 
curl "http://localhost:6001/add?n=b31&p=b" & curl "http://localhost:6002/add?n=ab32&p=ab" & curl "http://localhost:6003/add?n=bab33&p=bab"
wait 
curl "http://localhost:6001/add?n=ac41&p=ac" & curl "http://localhost:6002/add?n=bc42&p=bc" & curl "http://localhost:6003/add?n=baa43&p=baa"
wait 
curl "http://localhost:6001/add?n=cc51&p=cc" & curl "http://localhost:6002/add?n=cbb52&p=cbb" & curl "http://localhost:6003/add?n=bcc53&p=bcc"
wait 
curl "http://localhost:6001/remove?n=cc51&p=cc" & curl "http://localhost:6002/remove?n=cbb52&p=cbb" & curl "http://localhost:6003/remove?n=bcc53&p=bcc"
wait 
curl "http://localhost:6001/add?n=aab61&p=aab" & curl "http://localhost:6002/add?n=acc62&p=acc" & curl "http://localhost:6003/add?n=bac63&p=bac"
wait 
curl "http://localhost:6001/add?n=bbc71&p=bbc" & curl "http://localhost:6002/add?n=cab72&p=cab" & curl "http://localhost:6003/add?n=aac73&p=aac"
wait 
curl "http://localhost:6001/add?n=cac81&p=cac" & curl "http://localhost:6002/add?n=bbb82&p=bbb" & curl "http://localhost:6003/add?n=ab83&p=ab"
wait 
curl "http://localhost:6001/add?n=ba91&p=ba" & curl "http://localhost:6002/add?n=ca92&p=ca" & curl "http://localhost:6003/add?n=baa93&p=baa"
wait 
curl "http://localhost:6001/add?n=cc101&p=cc" & curl "http://localhost:6002/add?n=bb102&p=bb" & curl "http://localhost:6003/add?n=bcc103&p=bcc"
wait 
curl "http://localhost:6001/remove?n=cc101&p=cc" & curl "http://localhost:6002/remove?n=bb102&p=bb" & curl "http://localhost:6003/remove?n=bcc103&p=bcc"
wait 
curl "http://localhost:6001/add?n=aa111&p=aa" & curl "http://localhost:6002/add?n=cb112&p=cb" & curl "http://localhost:6003/add?n=c113&p=c"
wait 
curl "http://localhost:6001/add?n=bca121&p=bca" & curl "http://localhost:6002/add?n=cac122&p=cac" & curl "http://localhost:6003/add?n=acc123&p=acc"
wait 
curl "http://localhost:6001/add?n=acb131&p=acb" & curl "http://localhost:6002/add?n=cab132&p=cab" & curl "http://localhost:6003/add?n=bb133&p=bb"
wait 
curl "http://localhost:6001/add?n=bc141&p=bc" & curl "http://localhost:6002/add?n=a142&p=a" & curl "http://localhost:6003/add?n=cb143&p=cb"
wait 
curl "http://localhost:6001/add?n=cca151&p=cca" & curl "http://localhost:6002/add?n=bac152&p=bac" & curl "http://localhost:6003/add?n=cb153&p=cb"
wait 
curl "http://localhost:6001/remove?n=cca151&p=cca" & curl "http://localhost:6002/remove?n=bac152&p=bac" & curl "http://localhost:6003/remove?n=cb153&p=cb"
wait 
curl "http://localhost:6001/add?n=ccc161&p=ccc" & curl "http://localhost:6002/add?n=bba162&p=bba" & curl "http://localhost:6003/add?n=ba163&p=ba"
wait 
curl "http://localhost:6001/add?n=acc171&p=acc" & curl "http://localhost:6002/add?n=ab172&p=ab" & curl "http://localhost:6003/add?n=b173&p=b"
wait 
curl "http://localhost:6001/add?n=cc181&p=cc" & curl "http://localhost:6002/add?n=ac182&p=ac" & curl "http://localhost:6003/add?n=bb183&p=bb"
wait 
curl "http://localhost:6001/add?n=bca191&p=bca" & curl "http://localhost:6002/add?n=b192&p=b" & curl "http://localhost:6003/add?n=abc193&p=abc"
wait 
curl "http://localhost:6001/add?n=aac201&p=aac" & curl "http://localhost:6002/add?n=cbc202&p=cbc" & curl "http://localhost:6003/add?n=ab203&p=ab"
wait 
curl "http://localhost:6001/remove?n=aac201&p=aac" & curl "http://localhost:6002/remove?n=cbc202&p=cbc" & curl "http://localhost:6003/remove?n=ab203&p=ab"
wait 
curl "http://localhost:6001/add?n=baa211&p=baa" & curl "http://localhost:6002/add?n=baa212&p=baa" & curl "http://localhost:6003/add?n=cac213&p=cac"
wait 
curl "http://localhost:6001/add?n=b221&p=b" & curl "http://localhost:6002/add?n=bac222&p=bac" & curl "http://localhost:6003/add?n=ac223&p=ac"
wait 
curl "http://localhost:6001/add?n=acb231&p=acb" & curl "http://localhost:6002/add?n=caa232&p=caa" & curl "http://localhost:6003/add?n=bc233&p=bc"
wait 
curl "http://localhost:6001/add?n=c241&p=c" & curl "http://localhost:6002/add?n=ca242&p=ca" & curl "http://localhost:6003/add?n=bab243&p=bab"
wait 
curl "http://localhost:6001/add?n=bb251&p=bb" & curl "http://localhost:6002/add?n=bba252&p=bba" & curl "http://localhost:6003/add?n=aba253&p=aba"
wait 
curl "http://localhost:6001/remove?n=bb251&p=bb" & curl "http://localhost:6002/remove?n=bba252&p=bba" & curl "http://localhost:6003/remove?n=aba253&p=aba"
wait 
curl "http://localhost:6001/add?n=acb261&p=acb" & curl "http://localhost:6002/add?n=abc262&p=abc" & curl "http://localhost:6003/add?n=bbc263&p=bbc"
wait 
curl "http://localhost:6001/add?n=aab271&p=aab" & curl "http://localhost:6002/add?n=ba272&p=ba" & curl "http://localhost:6003/add?n=bc273&p=bc"
wait 
curl "http://localhost:6001/add?n=ccb281&p=ccb" & curl "http://localhost:6002/add?n=ca282&p=ca" & curl "http://localhost:6003/add?n=aac283&p=aac"
wait 
curl "http://localhost:6001/add?n=aab291&p=aab" & curl "http://localhost:6002/add?n=aa292&p=aa" & curl "http://localhost:6003/add?n=acc293&p=acc"
wait 
