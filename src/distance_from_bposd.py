from ldpc import bposd_decoder
import numpy as np
import src.helpers as helper


def bposd_decoder_distance_estimate(Hx : np.ndarray, Lx : np.ndarray, status_updates = False, num_shots: int = 100) -> int:
    best_distance = Hx.shape[1]

    for i, operator in enumerate(Lx):
        combined_matrix = np.vstack((Hx, operator))
        error_rates = [0.02]

        for rate in error_rates:
            bpd = bposd_decoder(
            parity_check_matrix = combined_matrix,
            error_rate = rate,
            channel_probs = [None],
            max_iter = combined_matrix.shape[1], # The maximum number of iterations for BP
            bp_method = "ms",
            ms_scaling_factor = 0, # Min sum scaling factor. If set to zero the variable scaling factor method is used
            osd_method = "osd_cs", # The OSD method. Choose from: 1) "osd_e", "osd_cs", "osd0"
            osd_order = 10 # The osd search depth
            )

            current_distance = Hx.shape[1]
            for _ in range(num_shots):
                syndrome = np.array( [0] * Hx.shape[0] + [1])
                new_estimate = sum(bpd.decode(syndrome))
                if new_estimate < current_distance:
                    current_distance = new_estimate

            if status_updates:
                print(f"For Logical of weight {sum(operator)} and error_rate {rate}, Distance: {current_distance}")

            if current_distance < best_distance:
                best_distance = current_distance


    return best_distance



def calculate_distance(H_x, H_z, use_x = True, status_updates = False) -> int:
    G = helper.standard_form(H_x, H_z)
    Lx, Lz = helper.find_logical_generators(G, helper.binary_rank(H_x))

    # only for css codes
    n = H_x.shape[1]
    Lx = np.delete(Lx, np.s_[n: ], axis=1)
    Lz = np.delete(Lz, np.s_[ :n], axis=1)

    if use_x:
        return bposd_decoder_distance_estimate(H_x, Lx, status_updates = status_updates, num_shots = 10)
    else:
        return bposd_decoder_distance_estimate(H_z, Lz, status_updates = status_updates, num_shots = 10)