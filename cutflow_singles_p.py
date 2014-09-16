#!/afs/desy.de/products/python/.amd64_rhel50/2.6/bin/python
from math import sqrt
from sys import exit
from ROOT import RooStats

# sample names according to: base/base_tag_sample.txt
#
##for tuning
samples =['DiBoson','TTbar','BosonJets','TopJets','STCfirst','NM1','NM2','NM3']


# we print a table without the last n lines
# with systematic error sys1 and sys2
# base is used for path/ and fileName as base/base_
# tag is NoPU,50PU,140PU
def Cutflow(path,base,tag,sys1,sys2,n,pick=[]):
	first=base+'_'+tag+'_'
	linesList=[]
	for s in samples:
		file = open(path+'/'+first+s+'.txt')
		linesList.append(file.readlines())
		file.close
	N=len(linesList[0])-n
	print base
	print ('%12s '+9*'%11s ') % (tag,'dibos','ttbar','B+jets','single t','sum bgrds','STC','NM1','NM2','NM3')
	for i in range(2,N):
		if len(pick)>0 and not i in pick: continue
		d=[] # data
		for k in range(len(linesList)):
			val = float(linesList[k][i].split('\t')[2])
			#val=val/3000.0*300.0
			d.append(val)
		what=linesList[0][i].split('\t')[0][7:]

		nbgrd=d[0]+d[1]+d[2]+d[3]
		print ('%2i: %12s '+9*'%10i ') % ( i,what,d[0],d[1],d[2],d[3],nbgrd,d[4],d[5],d[6],d[7])

		a=sqrt(nbgrd)
		b=sqrt(nbgrd*(1+sys1*sys1*nbgrd))
		c=sqrt(nbgrd*(1+sys2*sys2*nbgrd))
		a4sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[4],nbgrd,sys1)
		a5sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[5],nbgrd,sys1)
		a6sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[6],nbgrd,sys1)
		a7sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[7],nbgrd,sys1)
		a4sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[4],nbgrd,sys2)
		a5sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[5],nbgrd,sys2)
		a6sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[6],nbgrd,sys2)
		a7sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[7],nbgrd,sys2) 
                #print ('%19s '+48*' '+4*'%12f ') % ( 's/sqrt(b+('+str(sys1)+'*b)^2)',d[4]/b,d[5]/b,d[6]/b,d[7]/b )
		#print ('%19s '+48*' '+4*'%12f ') % ( 's/sqrt(b+('+str(sys2)+'*b)^2)',d[4]/c,d[5]/c,d[6]/c,d[7]/c )
		print ('%19s '+48*' '+4*'%12f ') % ( str(sys1),a4sys1,a5sys1,a6sys1,a7sys1 )
		print ('%19s '+48*' '+4*'%12f ') % ( str(sys2),a4sys2,a5sys2,a6sys2,a7sys2 )
        print		


Cutflow('September9_final','SingleS_P+DelphMET','140PU',0.15,0.25,1)


print RooStats.NumberCountingUtils.BinomialObsZ(321+121,121,0.5)
print RooStats.NumberCountingUtils.BinomialObsZ(193+90,90,0.5)

print RooStats.NumberCountingUtils.BinomialObsZ(228+59,59,0.5)
print RooStats.NumberCountingUtils.BinomialObsZ(166+45,45,0.5)

print RooStats.NumberCountingUtils.BinomialObsZ(379+42,42,0.5)
print RooStats.NumberCountingUtils.BinomialObsZ(337+391,337,0.15)

