from ldpc import bposd_decoder
import numpy as np
import src.helpers as helper


def bposd_decoder_distance_estimate(Hx : np.ndarray, Lx : np.ndarray, status_updates = False, num_shots: int = 10) -> int:
    for operator in Lx:
        distance = Hx.shape[1]
        print(
            f"shape of Hx: {Hx.shape}",
            f"shape of operator: {operator.shape}"
        )
        combined_matrix = np.vstack((Hx, operator))

        for error_rate in [0.05, 0.06]:

            bpd = bposd_decoder(
            parity_check_matrix = combined_matrix,
            error_rate = error_rate,
            channel_probs = [ None ],
            max_iter = combined_matrix.shape[1], # The maximum number of iterations for BP
            bp_method = "ms",
            ms_scaling_factor = 0, # Min sum scaling factor. If set to zero the variable scaling factor method is used
            osd_method = "osd_cs", #the OSD method. Choose from: 1) "osd_e", "osd_cs", "osd0"
            osd_order = 3 # the osd search depth
            )

            while num_shots > 0:
                syndrome = np.array( [0] * Hx.shape[0] + [1])
                new_estimate = sum(bpd.decode(syndrome))
                if new_estimate < distance:
                    distance = new_estimate
                num_shots -= 1

            if status_updates:
                print(f"For Logical {operator} and error rate: {error_rate}, Distance: {distance}")

    return 0



def calculate_distance(H_x, H_z, use_x = True, status_updates = False) -> int:
    G = helper.standard_form(H_x, H_z)
    Lx, Lz = helper.find_logical_generators(G, helper.binary_rank(H_x))

    print("shape of Lx: ", Lx.shape)
    print("shape of Lz: ", Lz.shape)

    # only for css codes
    n = H_x.shape[1]
    Lx = np.delete(Lx, np.s_[n: ], axis=1)
    Lz = np.delete(Lz, np.s_[ :n], axis=1)

    print("shape of Lx: ", Lx.shape)
    print("shape of Lz: ", Lz.shape)

    if use_x:
        distance = bposd_decoder_distance_estimate(H_x, Lx, status_updates = status_updates, num_shots = 10)
    else:
        distance = bposd_decoder_distance_estimate(H_z, Lz, status_updates = status_updates, num_shots = 10)

    return distance