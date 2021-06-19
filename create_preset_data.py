
import random
# create

def main():
    # read text file
    with open("./data/simple_wedding_rsvp/unique_ids.txt", 'r') as f:
        uids = [line.rstrip('\n') for line in f.readlines()]

    invites = []
    for i, id in enumerate(uids):
        d = {}
        d['id'] = id
        d['group_name'] = "Gruppe %d" % i
        d['people'] = []
        for k in range(random.randint(1, 5)):
            guest = {}
            guest['guest_name'] = "Gast %d" % k
            d['people'].append(guest)
        
        invites.append(d)
    
    # write to file
    with open("./data/simple_wedding_rsvp/preset_data_gen.py", 'w') as f:
        f.write("Invites = [\n")
        for invite in invites:
            f.write(str(invite) + ",\n")
        f.write("]")



if __name__ == '__main__':
    main() 