#!/afs/desy.de/products/python/.amd64_rhel50/2.6/bin/python
from math import sqrt
from sys import exit
from ROOT import RooStats

# sample names according to: base/base_tag_sample.txt
#
##for tuning
samples =['DiBoson','TTbar','BosonJets','TopJets','STCfirst','STOC','NM1','NM2','NM3']


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
	print ('%12s  '+10*'  & %11s ') % (tag,'diboson','ttbar','W/Z+jets','single t',
					   'sum bgrds','STC','STOC','NM1','NM2','NM3')
	print '\\\ \hline'
	for i in range(2,N):
		if len(pick)>0 and not i in pick: continue
		d=[] # data
		for k in range(len(linesList)):
			val = float(linesList[k][i].split('\t')[2])
			#val=val/3000.0*300.0
			d.append(val)
		what=linesList[0][i].split('\t')[0][11:]
		nbgrd=d[0]+d[1]+d[2]+d[3]
		#print ('%2i %12s '+9*' %10i ') % ( i,what,d[0],d[1],d[2],d[3],nbgrd,d[4],d[5],d[6],d[7])
		print ('%12s  '+10*' & %10f') % ( what,d[0],d[1],d[2],d[3],nbgrd,d[4],d[5],d[6],d[7],d[8])
		print '\\\ \hline'

		a=sqrt(nbgrd)
		b=sqrt(nbgrd*(1+sys1*sys1*nbgrd))
		c=sqrt(nbgrd*(1+sys2*sys2*nbgrd))
		a4sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[4],nbgrd,sys1)
		a5sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[5],nbgrd,sys1)
		a6sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[6],nbgrd,sys1)
		a7sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[7],nbgrd,sys1)
		a4sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[4],nbgrd,sys2)
		a8sys1 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[8],nbgrd,sys1)

		a5sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[5],nbgrd,sys2)
		a6sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[6],nbgrd,sys2)
		a7sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[7],nbgrd,sys2) 
		a8sys2 = RooStats.NumberCountingUtils.BinomialObsZ(nbgrd+d[8],nbgrd,sys2) 
		print ('%19s '+48*' '+5*'%12f ') % ( str(sys1),a4sys1,a5sys1,a6sys1,a7sys1,a8sys1 )
		print ('%19s '+48*' '+5*'%12f ') % ( str(sys2),a4sys2,a5sys2,a6sys2,a7sys2,a8sys2 )
        print		



#print the table header and stuff

print '  \\begin{sidewaystable}[htdp]'
print '  \caption{bla}'
print '  \\begin{center}'
print '  \\begin{tabular}{|l|c|c|c|c|c|c|c|c|c|c|}  \hline'

Cutflow('September15_noHTcut','SingleS_P+DelphMET','140PU',0.25,0.5,1)


print '  \end{tabular}'
print '  \end{center}'
print '  \end{sidewaystable}'
