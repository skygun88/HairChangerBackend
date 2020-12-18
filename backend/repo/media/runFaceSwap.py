import sys
import os
import shutil
import time
import datetime
import sqlite3

def makeImgCopy(filePath, number):
    fileType = filePath.split('.')[-1]
    FileParsed = filePath.replace(fileType, '')

    copyList = []
    for i in range(number):
        tempFileName = FileParsed+f'{i}.'+fileType
        copyList.append(tempFileName)
        shutil.copyfile(filePath, tempFileName)
    return copyList

def removeFiles(copyList):
    for file in copyList:
        os.remove(file)

def main(idx, oriFacePath, oriHairPath, resultPath, iters):
    success = True
    start = time.time()
    iterations = str(iters)

    ''' Step 0: Path and Variable Definition '''
    faceswapPath = '/home/ubuntu/faceswap/faceswap.py'
    currtime = str(datetime.datetime.now())
    currtime = currtime.replace(' ', '_')
    tempPath = currtime + '/'
    currPath = os.path.dirname(os.path.realpath(__file__)) + '/'
    srcPath = 'src/'
    extPath = 'extract/'
    facePath = 'face/'
    hairPath = 'hair/'

    convertedPath = 'converted/' + tempPath
    modelPath = 'model/' + tempPath

    srcFacePath = currPath+srcPath+facePath+tempPath
    srcHairPath = currPath+srcPath+hairPath+tempPath

    extFacePath = currPath+extPath+facePath+tempPath
    extHairPath = currPath+extPath+hairPath+tempPath

    pathList = [convertedPath, modelPath, srcFacePath, srcHairPath, extFacePath, extHairPath]
    
    for p in pathList:
        print(p)
        os.makedirs(p)

    ''' Link to DB '''
    conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
    cur = conn.cursor()

    ''' Copy the hair & face files to temporary directory '''
    # Hair copies
    hairFileName = oriHairPath.split('/')[-1]
    shutil.copyfile(oriHairPath, srcHairPath+hairFileName)

    # Face copies
    for f in os.listdir(oriFacePath):
        if not os.path.isdir(oriFacePath+'/'+f):
            shutil.copyfile(oriFacePath+'/'+f, srcFacePath+f)

    ''' Step 1: Image Proliferation'''
    # Hair image proliferation
    hairFile = os.listdir(srcHairPath)[0]
    hairFilePath = srcHairPath + hairFile 
    hairCopyList = makeImgCopy(hairFilePath, 25)
    hairCopyList.append(hairFilePath)

    # Face image proliferation
    faceCopyList = []
    faces = os.listdir(srcFacePath)
    for f in faces:
        faceCopyList.extend(makeImgCopy(srcFacePath + f, 25))
        faceCopyList.append(srcFacePath + f)
    
    print("Step 1 - Image Proliferation is done")


    ''' Step 2: Face Extraction '''
    try:
        os.system(f'python {faceswapPath} extract -i {srcFacePath} -o {extFacePath} -L INFO')
        os.system(f'python {faceswapPath} extract -i {srcHairPath} -o {extHairPath} -L INFO')
        faceAlignmentPath = srcFacePath + 'alignments.fsa'
        hairAlignmentPath = srcHairPath + 'alignments.fsa'
        print("Step 2 - Face Extraction is done")

        cur.execute(f"UPDATE requests_requestinfo SET progress=2 WHERE idx={idx};")
        conn.commit()

        ''' Step 3: Train '''
        os.system(f'python {faceswapPath} train -A {extHairPath} -ala {hairAlignmentPath} -B {extFacePath} -alb {faceAlignmentPath} -m {modelPath} -it {iterations} -L INFO')
        print("Step 3 - Train is done")

        cur.execute(f"UPDATE requests_requestinfo SET progress=3 WHERE idx={idx};")
        conn.commit()

        ''' Step 4: Convert '''
        os.system(f'python {faceswapPath} convert -i {srcHairPath} -al {hairAlignmentPath} -o {convertedPath} -m {modelPath} -L INFO')
        print("Step 4 - Convert is done")

        result_file = os.listdir(convertedPath)[0]
        shutil.copyfile(convertedPath+result_file, resultPath)

        cur.execute(f"UPDATE requests_requestinfo SET progress=4 WHERE idx={idx};")
        conn.commit()

        ''' Step 5: Images to Video '''
    except Exception as e:
        cur.execute(f"UPDATE requests_requestinfo SET progress=-1 WHERE idx={idx};")
        conn.commit()
        success = False
        print(f'error occurs.... \n{e}')


    ''' Remove temporary files '''
    os.system(f'rm -rf result/{currtime}* model/{currtime}* extract/face/{currtime}* extract/hair/{currtime}* src/hair/{currtime}* src/face/{currtime}* converted/{currtime}*')

    print('done')
    executionTime = time.time() - start

    with open('testLog.txt', 'a') as output:
        output.write(f'Start time : {currtime}, Iteration : {iters}\n')
        output.write(f'OriFacePath : {oriFacePath}\n')
        output.write(f'Hair : {oriHairPath}\n')
        output.write(f'Result Path : {resultPath}\n')
        output.write(f'Success : {success}\n')
        output.write(f'Execution time -- {executionTime} sec / {executionTime/60} min / {executionTime/3600} hour\n')
        output.write(f'----------------------------------\n')
        output.close()

if __name__ == '__main__':
    idx, facePath, hairPath, resultPath, iters = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    main(idx, facePath, hairPath, resultPath, iters)
