def npyQuestion():
    npyH = input("Do you already have a pre-processed tensor as .npy file? (yes or no)")
    if any(npyH.lower() == f for f in ["yes", 'y', '1', 'ye']):
        return(True)
        break
    elif any(npyH.lower() == f for f in ['no', 'n', '0']):
        return(False)
        break
    else:
        print('Please enter yes or no')

def npyPath():
    npyP = input("Path of the .npy file:")
    if len(npyP)>0:
        return(npyP)
        break
    else:
        print('Please enter a path')

def matPath():
    matP = input("Path of the directory with all the .mat files:")
    if len(matP)>0:
        return(matP)
        break
    else:
        print('Please enter a path directory')

def SVDquestion():
    svd = input("Do you want to reduce the solutions dimensions with SVD? (yes or no)")
    if any(svd.lower() == f for f in ["yes", 'y', '1', 'ye']):
        return(True)
        break
    elif any(svd.lower() == f for f in ['no', 'n', '0']):
        return(False)
        break
    else:
        print('Please enter yes or no')

def nbComp():
    nComp = int(input("Number of component for the SVD:"))
    if nComp>0:
        return(nComp)
        break
    else:
        print('Please enter a number of component')

def npySave():
    npyW = input("Do you want to save the pre-processed data as a .npy file? (yes or no)")
    if any(npyW.lower() == f for f in ["yes", 'y', '1', 'ye']):
        return(True)
        break
    elif any(npyW.lower() == f for f in ['no', 'n', '0']):
        return(False)
        break
    else:
        print('Please enter yes or no')

def npySavePath():
    npySP = input("Give the path and name of the new saved .npy file")
    if npySP.endswith('.npy')>0:
        return(npySP)
        break
    else:
        print('Please enter a path with the name of the file and .npy')