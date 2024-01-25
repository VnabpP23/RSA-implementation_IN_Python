
import random
import math


def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus  # Ensure base is within the modulus

    while exponent > 0:
        # If exponent is odd, multiply result with base
        if exponent % 2 == 1:
            result = (result * base) % modulus

        # Update base to the square of itself
        base = (base * base) % modulus

        # Divide the exponent by 2
        exponent //= 2

    return result
# Large Prime Generation for RSA	
# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
					31, 37, 41, 43, 47, 53, 59, 61, 67,
					71, 73, 79, 83, 89, 97, 101, 103,
					107, 109, 113, 127, 131, 137, 139,
					149, 151, 157, 163, 167, 173, 179,
					181, 191, 193, 197, 199, 211, 223,
					227, 229, 233, 239, 241, 251, 257,
					263, 269, 271, 277, 281, 283, 293,
					307, 311, 313, 317, 331, 337, 347, 349]


def nBitRandom(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)


def getLowLevelPrime(n):
	'''Generate a prime candidate divisible 
	by first primes'''
	while True:
		# Obtain a random number
		pc = nBitRandom(n)

		# Test divisibility by pre-generated
		# primes
		for divisor in first_primes_list:
			if pc % divisor == 0 and divisor**2 <= pc:
				break
		else:
			return pc


def isMillerRabinPassed(mrc):
	'''Run 20 iterations of Rabin Miller Primality test'''
	maxDivisionsByTwo = 0
	ec = mrc-1
	while ec % 2 == 0:
		ec >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * ec == mrc-1)

	def trialComposite(round_tester):
		if pow(round_tester, ec, mrc) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * ec, mrc) == mrc-1:
				return False
		return True

	# Set number of trials here
	numberOfRabinTrials = 20
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2, mrc)
		if trialComposite(round_tester):
			return False
	return True
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"The modular inverse does not exist for {a} (mod {m})")
    else:
        return x % m

def gen_pq():
		
    pq=[]
    for	i in range(2):
        while True:
            n = 1024
            prime_candidate = getLowLevelPrime(n)	
            if not isMillerRabinPassed(prime_candidate):	
                continue	
            else:	
                pq.append(prime_candidate)
        
                break
    return pq

#Genarated large prime(p,q)
	
p=0
q=0
p=gen_pq()[0]
q=gen_pq()[1]

#Public key pair (e,n)
n=p*q
phi_n=(p-1)*(q-1)
e = 65537
#Secret key pair(d,n)
d=mod_inverse(e,phi_n)


file=open("data_to_Encrypt.txt","r")
msg=file.readline()
msgList=[]
for i in msg:
    msgList.append(ord(i))      
#Encrypting the msg
def encription():
    encripted_data=[modular_exponentiation(j,e,n) for j in msgList]
    return encripted_data
          
#Decrypting the encrupted data
def dycription():
    en=encription()
    return [modular_exponentiation(k,d,n) for k in en]

#turning the dycripted  data into text
def msger():
    return "".join(chr(cr) for cr in dycription())  
filewrite = open("Decrypted_data.txt", "w")
filewrite.write(msger())
filewrite.close()

    
    
