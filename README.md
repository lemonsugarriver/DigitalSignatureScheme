Relaxation done in this assignment.
1)	Instead of calculating e' as H(m||r'), e' is calculated as e' = e - v
	Consider e'' = H(m || r')

2)	A(Client) sends signed message to B as m,e',s',e''

3)	In verification process, B calculates r* in the same way as provided by assignment
	if H(m||r*) == e'' 
	then	return True
	else	return False
 
