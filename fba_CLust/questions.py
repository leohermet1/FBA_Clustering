def npyQuestion():
    i = 0
    while i < 5:
        npyH = input("Do you already have a pre-processed tensor as .npy file? (yes or no)")
        if any(npyH.lower() == f for f in ["yes", 'y', '1', 'ye']):
            return(True)
            break
        elif any(npyH.lower() == f for f in ['no', 'n', '0']):
            return(False)
            break
        else:
            i += 1
            if i < 5:
                print('Please enter yes or no')
            else:
                print("Nothing done")

def npyPath():
    i = 0
    while i < 5:
        npyP = input("Path of the .npy file:")
        if len(npyP)>0:
            return(npyP)
            break
        else:
            i += 1
            if i < 5:
                print('Please enter a path')
            else:
                print("Nothing done")

def matPath():
    i = 0
    while i < 5:
        matP = input("Path of the directory with all the .mat files:\n"
                     "Warning: the name of each file has to contain the id of the patient as an integer at the 22th character of the name "
                     "and end with \".mat\".\n"
                     "Example: \"modelPatient_Sampled_10_Mean.mat\"")
        if len(matP)>0:
            return(matP)
            break
        else:
            i += 1
            if i < 5:
                print('Please enter a path directory')
            else:
                print("Nothing done")

def SVDquestion():
    i = 0
    while i < 5:
        svd = input("Do you want to reduce the solutions dimensions with SVD? (yes or no)")
        if any(svd.lower() == f for f in ["yes", 'y', '1', 'ye']):
            return(True)
            break
        elif any(svd.lower() == f for f in ['no', 'n', '0']):
            return(False)
            break
        else:
            i += 1
            if i < 5:
                print('Please enter yes or no')
            else:
                print("Nothing done")


def nbComp():
    i = 0
    while i < 5:
        nComp = int(input("Number of component for the SVD:"))
        if nComp>0:
            return(nComp)
            break
        else:
            i += 1
            if i < 5:
                print('Please enter a number of component')
            else:
                print("Nothing done")

def npySave():
    i = 0
    while i < 5:
        npyW = input("Do you want to save the pre-processed data as a .npy file? (yes or no)")
        if any(npyW.lower() == f for f in ["yes", 'y', '1', 'ye']):
            return(True)
            break
        elif any(npyW.lower() == f for f in ['no', 'n', '0']):
            return(False)
            break
        else:
            i += 1
            if i < 5:
                print('Please enter yes or no')
            else:
                print("Nothing done")

def npySavePath():
    i = 0
    while i < 5:
        npySP = input("Give the path and name of the new saved .npy file")
        if npySP.endswith('.npy')>0:
            return(npySP)
            break
        else:
            i += 1
            if i < 5:
                print('Please enter a path with the name of the file and .npy')
            else:
                print("Nothing done")