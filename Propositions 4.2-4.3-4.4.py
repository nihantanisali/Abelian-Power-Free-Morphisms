#!/usr/bin/env python
# coding: utf-8

# In[28]:


##checks abelian power freenes
def avoids_abelian_k_power(sequence: str, k: int) -> bool:
    n = len(sequence)
    
    
    for block_len in range(1, n // k + 1):
        for start in range(n - block_len * k + 1):
            blocks = [sequence[start + j * block_len : start + (j + 1) * block_len] for j in range(k)]
            if all(sorted(blocks[0]) == sorted(b) for b in blocks):
                return False
    
    return True



##given a sequence extends it to all valid continuations
def extend_partial_sequence(n: int, k: int, forbidden_substrings: list[str], current_sequence: str, results: list[str]) -> None:
    """
    Geri izlemeli (backtracking) şekilde diziyi kurar.
    Kurallar ihlal edilirse o dal erken kesilir.
    """
    if len(current_sequence) == n:
        results.append(current_sequence)
        return

    for bit in "01":
        new_sequence = current_sequence + bit

        #checks forbidden patterns  
        if any(pat in new_sequence for pat in forbidden_substrings):
            continue

        #cheks is abelian k power free
        if not avoids_abelian_k_power(new_sequence, k):
            continue

        #continues if ok
        extend_partial_sequence(n, k, forbidden_substrings, new_sequence, results)
        
        
##generates all valid sequences of given lengths
def generate_valid_binary_sequences(n: int, forbidden_substrings: list[str], k: int) -> list[str]:
    
    results = []
    extend_partial_sequence(n, k, forbidden_substrings, "", results)
    return results

#######################################################################

forbidden_substrings_prop_4_2 = ["11"]
forbidden_substrings_prop_4_3 = ["11","000"]
forbidden_substrings_prop_4_4 = ["11","0000"]

k_prop_4_2=4
k_prop_4_3=5
k_prop_4_4=5


valid_sequences_prop_4_2_length17 = generate_valid_binary_sequences(17, forbidden_substrings_prop_4_2, k_prop_4_2)
valid_sequences_prop_4_2_length18 = generate_valid_binary_sequences(18, forbidden_substrings_prop_4_2, k_prop_4_2)


valid_sequences_prop_4_3_length24 = generate_valid_binary_sequences(24, forbidden_substrings_prop_4_3, k_prop_4_3)
valid_sequences_prop_4_3_length25 = generate_valid_binary_sequences(25, forbidden_substrings_prop_4_3, k_prop_4_3)


valid_sequences_prop_4_4_length77 = generate_valid_binary_sequences(77, forbidden_substrings_prop_4_4, k_prop_4_4 )
valid_sequences_prop_4_4_length78 = generate_valid_binary_sequences(78, forbidden_substrings_prop_4_4, k_prop_4_4)








######################################################################
print('============= Proposition 4.2 ============= ')
print("The sequences of length 17 avoiding",forbidden_substrings_prop_4_2 ,"are/is" ,valid_sequences_prop_4_2_length17  )
print("The sequences of length 18 avoiding",forbidden_substrings_prop_4_2 ,"are/is" ,valid_sequences_prop_4_2_length18  )



######################################################################
print('============= Proposition 4.3 ============= ')

print("The sequences of length 24 avoiding",forbidden_substrings_prop_4_3 ,"are/is" ,valid_sequences_prop_4_3_length24  )
print("The sequences of length 25 avoiding",forbidden_substrings_prop_4_3 ,"are/is" ,valid_sequences_prop_4_3_length25  )



######################################################################
print('============= Proposition 4.4 ============= ')

print("The sequences of length 77 avoiding",forbidden_substrings_prop_4_4 ,"are/is" ,valid_sequences_prop_4_4_length77  )
print("The sequences of length 78 avoiding",forbidden_substrings_prop_4_4 ,"are/is" ,valid_sequences_prop_4_4_length78  )

    
    

