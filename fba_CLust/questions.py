def npyQuestion():
    i = 0
    while i < 2:
        npyH = input("Do you have a .npy matrix? (yes or no)")
        if any(npyH.lower() == f for f in ["yes", 'y', '1', 'ye']):
            return(True)
            break
        elif any(npyH.lower() == f for f in ['no', 'n', '0']):
            return(False)
            break
        else:
            i += 1
            if i < 2:
                print('Please enter yes or no')
            else:
                print("Nothing done")

def npyPath():
    i = 0
    while i < 2:
        npyP = input("Path of the .npy file:")
        if len(npyP)>0:
            return (npyP)
            break
        else:
            i += 1
            if i < 2:
                print('Please enter a path')
            else:
                print("Nothing done")

def matPath():
    i = 0
    while i < 2:
        matP = input("Path of the directory with all the .mat files:")
        if len(matP)>0:
            return (matP)
            break
        else:
            i += 1
            if i < 2:
                print('Please enter a path directory')
            else:
                print("Nothing done")

def SVDquestion():
    i = 0
    while i < 2:
        svd = input("Do you want to reduce the solutions dimensions with SVD? (yes or no)")
        if any(svd.lower() == f for f in ["yes", 'y', '1', 'ye']):
            return(True)
            break
        elif any(svd.lower() == f for f in ['no', 'n', '0']):
            return(False)
            break
        else:
            i += 1
            if i < 2:
                print('Please enter yes or no')
            else:
                print("Nothing done")

def nbComp():
    i = 0
    while i < 2:
        nComp = int(input("Number of component for the SVD:"))
        if len(nComp)>0:
            return (nComp)
            break
        else:
            i += 1
            if i < 2:
                print('Please enter an number of component')
            else:
                print("Nothing done")

def npySave():
    i = 0
    while i < 2:
        npyW = input("Do you want to save the pre-processed data as a .npy file? (yes or no)")
        if any(npyW.lower() == f for f in ["yes", 'y', '1', 'ye']):
            return(True)
            break
        elif any(npyW.lower() == f for f in ['no', 'n', '0']):
            return(False)
            break
        else:
            i += 1
            if i < 2:
                print('Please enter yes or no')
            else:
                print("Nothing done")