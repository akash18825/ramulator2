'''
# Row-Hit Friendly
M = 1024
K = 1024
elem = 4

A_base = 0x00000000
B_base = 0x10000000
C_base = 0x20000000

with open("gemv_rowhit.trace", "w") as f:
    for i in range(M):
        for k in range(K):
            # Sequential access inside row
            f.write(f"LD 0x{A_base + (i*K + k)*elem:x}\n")
            f.write(f"LD 0x{B_base + k*elem:x}\n")
        f.write(f"ST 0x{C_base + i*elem:x}\n")
'''

'''
#Row-Conflict Heavy GEMV
M = 1024
K = 1024
elem = 4

A_base = 0x00000000
B_base = 0x10000000
C_base = 0x20000000

with open("gemv_rowconflict.trace", "w") as f:
    for i in range(M):
        for k in range(K):
            # Jump across rows instead of staying in same row
            f.write(f"LD 0x{A_base + (k*M + i)*elem:x}\n")
            f.write(f"LD 0x{B_base + k*elem:x}\n")
        f.write(f"ST 0x{C_base + i*elem:x}\n")
'''

'''
N = 500000
elem = 4
ROW_STRIDE = 8192  # try 8KB, 16KB, 32KB if needed

base = 0x00000000

with open("pure_row_thrash.trace", "w") as f:
    for i in range(N):
        f.write(f"LD 0x{base:x}\n")
        f.write(f"LD 0x{base + ROW_STRIDE:x}\n")
'''

# Tiled GEMV for Row Buffer Study

M = 1024
K = 1024
TILE = 256
elem = 4  # bytes per element (float/int)

# Base addresses (separated regions)
A_base = 0x00000000
B_base = 0x10000000
C_base = 0x20000000

output_file = "gemv_tiled_256.trace"

with open(output_file, "w") as f:

    for i0 in range(0, M, TILE):

        # Process all K tiles first (loads)
        for k0 in range(0, K, TILE):

            for i in range(i0, min(i0 + TILE, M)):
                for k in range(k0, min(k0 + TILE, K)):

                    # Load A[i][k]
                    addr_A = A_base + (i * K + k) * elem
                    f.write(f"LD {addr_A}\n")

                    # Load B[k]
                    addr_B = B_base + k * elem
                    f.write(f"LD {addr_B}\n")

        # Store result C[i] after full accumulation
        for i in range(i0, min(i0 + TILE, M)):
            addr_C = C_base + i * elem
            f.write(f"ST {addr_C}\n")

print(f"Trace generated: {output_file}")
