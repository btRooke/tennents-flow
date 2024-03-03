from pubsim.PubMap import PubMap

def pubsim_transition_to_frontend(transition_matrix):
    movements = {}

    for pub1, row in transition_matrix.iterrows():
        movements[pub1] = {};


        for pub2, value in row.items():
            if value == 0:
                continue

            movements[pub1][pub2] = value;

    return movements

def pubsim_revenue_to_frontend(revenue_matrix):
    return revenue_matrix