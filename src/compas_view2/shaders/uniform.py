from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from time import time
import math
import sys


# representation of a uniform block
class UniformBlock:
     def __init__(self, shaderProg, name):
        self.shaderProg = shaderProg 
        self.name = name
     def Link(self, bindingPoint):
        self.bindingPoint = bindingPoint
        self.noOfUniforms = glGetProgramiv(self.shaderProg, GL_ACTIVE_UNIFORMS)
        self.maxUniformNameLen = glGetProgramiv(self.shaderProg, GL_ACTIVE_UNIFORM_MAX_LENGTH)
        self.index = glGetUniformBlockIndex(self.shaderProg, self.name)
        intData = np.zeros(1, dtype=int)
        glGetActiveUniformBlockiv(self.shaderProg, self.index, GL_UNIFORM_BLOCK_ACTIVE_UNIFORMS, intData)
        self.count = intData[0]
        self.indices = np.zeros(self.count, dtype=int)
        glGetActiveUniformBlockiv(self.shaderProg, self.index, GL_UNIFORM_BLOCK_ACTIVE_UNIFORM_INDICES, self.indices)
        self.offsets = np.zeros(self.count, dtype=int)
        glGetActiveUniformsiv(self.shaderProg, self.count, self.indices, GL_UNIFORM_OFFSET, self.offsets)
        self.size = 0
        strLengthData = np.zeros(1, dtype=int)
        arraysizeData = np.zeros(1, dtype=int)
        typeData = np.zeros(1, dtype='uint32')
        nameData = np.chararray(self.maxUniformNameLen+1)
        self.namemap = {}
        self.dataSize = 0 
        for inx in range(0, len(self.indices)):
            glGetActiveUniform( self.shaderProg, self.indices[inx], self.maxUniformNameLen, strLengthData, arraysizeData,     typeData, nameData.data )
            name = nameData.tostring()[:strLengthData[0]]
            self.namemap[name] = inx
            self.dataSize = max(self.dataSize, self.offsets[inx] + arraysizeData * 16) 
        glUniformBlockBinding(self.shaderProg, self.index, self.bindingPoint)
        print('\nuniform block %s size:%4d' % (self.name, self.dataSize))
        for uName in self.namemap:
            print( '    %-40s index:%2d    offset:%4d' % (uName, self.indices[self.namemap[uName]], self.offsets    [self.namemap[uName]]) ) 

# representation of a uniform block buffer
class UniformBlockBuffer:
    def __init__(self, ub):
        self.namemap = ub.namemap
        self.offsets = ub.offsets
        self.bindingPoint = ub.bindingPoint
        self.object = glGenBuffers(1)
        self.dataSize = ub.dataSize
        glBindBuffer(GL_UNIFORM_BUFFER, self.object)
        dataArray = np.zeros(self.dataSize//4, dtype='float32')
        glBufferData(GL_UNIFORM_BUFFER, self.dataSize, dataArray, GL_DYNAMIC_DRAW)
    def BindToTarget(self):
        glBindBuffer(GL_UNIFORM_BUFFER, self.object)
        glBindBufferBase(GL_UNIFORM_BUFFER, self.bindingPoint, self.object)
    def BindDataFloat(self, name, dataArr):
        glBindBuffer(GL_UNIFORM_BUFFER, self.object)
        dataArray = np.array(dataArr, dtype='float32')
        glBufferSubData(GL_UNIFORM_BUFFER, self.offsets[self.namemap[name]], len(dataArr)*4, dataArray)