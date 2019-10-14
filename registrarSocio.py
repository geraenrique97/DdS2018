import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import cv2

class sistema:
    def __init__(self):
        self.__socios=list()

    def obtenerClases(self,userName, password,sucursal):
        dato = {
            'user':'nicmalegre',
            'password':'40801010',
            'database':'energym2',
            'host':'localhost'
        } 

        conexion = mysql.connector.connect(** dato)
        cursor = conexion.cursor() 
        consulta = "SELECT * FROM clase where sucursal=%s"
        suc=(sucursal,)
        cursor.execute(consulta, suc)
        clases= cursor.fetchall()
        LTClases=list()
        for row in clases:
            
            cursor = conexion.cursor()
            consulta = "SELECT * FROM turno where idClase=%s"
            idclase=(row[0],)
            cursor.execute(consulta, idclase)
            turnos= cursor.fetchall()
            
            if row[1]!='Complemento':
                listTurnos=list()
                for j in turnos:
                    unTurno=turno(j[2],j[3],j[4])
                    listTurnos.append(unTurno)
            else:
                listTurnos=None
            LTClases.append(clase(row[1],row[3],listTurnos))
            del listTurnos
        cursor.close()
        conexion.close()


        return LTClases
    
    def guardarSocio(self, socio):
        self.__socios.append(socio)
        dato = {
            'user':'root',
            'password':'',
            'database':'energym2',
            'host':'localhost'
        } 
        conexion = mysql.connector.connect(** dato)
        cursor = conexion.cursor()
        datosTCli=(socio.getNombre(), socio.getDNI(),socio.getTelefono(), socio.getEmail(), socio.getDomicilio(),socio.getSexo(),socio.getAntMed(), socio.getSaldo(),)
        insertSocio = "INSERT INTO socio(nombre, dni, telefono, email, domicilio, sexo, antecmed, saldo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        
        turno=''
        if socio.getServicios()[0].getClase()!='Complemento':
            turno=socio.getServicios()[0].getTurno().getHorario()
        datosTServ=(socio.getNombre(), 
            socio.getServicios()[0].getClase(),
            turno,
            socio.getServicios()[0].getSucursal(),)
        insertServ="INSERT INTO asiste(socio, clase, turno, sucursal) VALUES(%s,%s,%s,%s)"
        
        try:
            cursor.execute(insertSocio, datosTCli)
            conexion.commit()
            cursor.execute(insertServ, datosTServ)
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except:
            cursor.close()
            conexion.close()
            return False

class clase:
    def __init__(self,nombre,precio, turnos):
        self.__nombre=nombre
        self.__precio=precio
        self.__turnos=turnos
    def getTurnos(self):
        return self.__turnos

    def getNombre(self):
        return self.__nombre

    def getPrecio(self):
        return self.__precio

    def setTurnos(self,turnos):
        self.__turnos=turnos

class turno:
    def __init__(self,dia, hora, cupos):
        self.__dia=dia
        self.__hora=hora
        self.__cupos=cupos

    def getCupos(self):
        return self.__cupos

    def getHorario(self):
        return (self.__dia+' '+self.__hora)


class socio:
    def __init__(self):
        self.__nombre=None
        self.__dni=None
        self.__email=None
        self.__telefono=None
        self.__domicilio=None
        self.__sexo=None
        self.__foto=None
        self.__antMed=None
        self.__saldo=0
        self.__servicios=list()
   
    def setDatos(self, nombre, dni, email, tel, domicilio, sexo, foto, antMed):
        self.__nombre=nombre
        self.__dni=dni
        self.__email=email
        self.__telefono=tel
        self.__domicilio=domicilio
        self.__sexo=sexo
        self.__foto=foto
        self.__antMed=antMed
        
    def acumularSaldo(self,monto):
        self.__saldo=self.__saldo+monto

    def agregarServicio(self,clase,turno,sucursal):
        servContratado=servicio()
        servContratado.setClase(clase)
        servContratado.setTurno(turno)        
        servContratado.setSucursal(sucursal)
        servContratado.setFecha(time.strftime("%d/%m/%y"))
        self.__servicios.append(servContratado)

    #-----------------------------------------------
    def getNombre(self):
        return self.__nombre
    def getDNI(self):
        return self.__dni
    def getEmail(self):
        return self.__email
    def getTelefono(self):
        return self.__telefono
    def getDomicilio(self):
        return self.__domicilio
    def getSexo(self):
        return self.__sexo
    def getFoto(self):
        return self.__foto
    def getAntMed(self):
        return self.__antMed
    def getSaldo(self):
        return self.__saldo
    def getServicios(self):
        return self.__servicios
    #------------------------------------------------
class servicio:
    def __init__(self):
        self.__clase=None
        self.__turno=None
        self.__sucursal=None
        self.__fecha=None

    def setClase(self, clase):
        self.__clase=clase
    def setTurno(self, turno):
        self.__turno=turno
    def setSucursal(self, suc):
        self.__sucursal=suc
    def setFecha(self, fecha):
        self.__fecha=fecha

    #--------------------------
    def getClase(self):
        return self.__clase
    def getTurno(self):
        return self.__turno
    def getSucursal(self):
        return self.__sucursal
    def getFecha(self):
       return self.__fecha
    #--------------------------

class CTRLsesion:
    def __init__(self):
        self.__usuario='secretaria'
        self.__contraseña='password'
        self.__sucursal=1
        
    def getUsuario(self):
        return self.__usuario

    def getPassword(self):
        return self.__contraseña

    def getSucursal(self):
        return self.__sucursal

class CTRLregistrarSocio:
    def create(self):
        pass

    def destroy(self): 
        pass

    def ejecutar(self):        
        app = QApplication(sys.argv)

        UI=UIregistrarSocio()
        UI.show() 
        
        userName=CTRLsesion().getUsuario()
        password=CTRLsesion().getPassword()
        suc=CTRLsesion().getSucursal()
        LTClases=sistema().obtenerClases(userName,password,suc)

        clasesDisp=list()
        for i in range(len(LTClases)):
            unaClase=LTClases[i]
            if unaClase.getNombre()!='Complemento': 
                LTTurno=unaClase.getTurnos()
                turnosDisp=list()
                for j in range(len(LTTurno)):
                    unTurno=LTTurno[j]
                    cuposTurno=unTurno.getCupos()
                    if cuposTurno>0:
                        turnosDisp.append(unTurno)
                if len(turnosDisp)>0:
                    unaClase.setTurnos(turnosDisp)
                    clasesDisp.append(unaClase)
                del turnosDisp
            else:
                clasesDisp.append(unaClase)

        UI.mostrarClases(clasesDisp)
        app.exec_()
        
    def registrarsocio(self, datos):

        nuevoSocio=socio()
         #nombre, dni, email, telefono, sexo, foto, antMedicos      
        nuevoSocio.setDatos(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7])
        unaClase=datos[len(datos)-2] 
        monto=unaClase.getPrecio()
        nuevoSocio.acumularSaldo(monto)
        unTurno=datos[len(datos)-1]
        
        suc=CTRLsesion().getSucursal() 
        nuevoSocio.agregarServicio(unaClase.getNombre(), unTurno, suc)
         
        exito=sistema().guardarSocio(nuevoSocio)

        return exito      
        
class UIregistrarSocio(QMainWindow, CTRLregistrarSocio):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("registrarsocio.ui", self)
        self.clases=list() 
        self.actividad.currentTextChanged.connect(self.seleccionarClase)
        self.botonGuardar.clicked.connect(self.confirmarDatos)
        self.botonCancelar.clicked.connect(self.cancelarOp)
        self.botonFoto.clicked.connect(self.capturarFoto)
        foto=QPixmap('sinfoto.png').scaled(135,135,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.labelFoto.setPixmap(foto)

    def capturarFoto(self):
        cap = cv2.VideoCapture(0)
        leido, frame = cap.read()

        if leido == True:
            cv2.imwrite("foto.png", frame)

        cap.release()
        foto=QPixmap('foto.png').scaled(135,135,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.labelFoto.setPixmap(foto)


    def controlCompleto(self):
        
        if self.nombre.text()!='' and self.dni.text()!='':
            self.nombre.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.dni.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.dni.setMaxLength(8)
            return True
        else:
            if self.nombre.text()=='':
                self.nombre.setStyleSheet("background-color: rgb(255, 255, 127);")
            if len(self.dni.text())<8:
                self.dni.setStyleSheet("background-color: rgb(255, 255, 127);")
            return False

    def mostrarClases(self,clasesDisp):
        self.clases=clasesDisp
        for unaClase in clasesDisp:
            self.actividad.addItem(unaClase.getNombre())
        
    def seleccionarClase(self):
        if self.actividad.currentText()!='Complemento':
            self.labelTurno.setVisible(True)
            self.turno.setVisible(True)
            self.mostrarTurnos(self.actividad.currentText())
        else:
            self.turno.setVisible(False)
            self.labelTurno.setVisible(False)
            self.turno.clear()

    def mostrarTurnos(self,claseSelec): 
        self.turno.clear()
        for unaClase in self.clases:
            if unaClase.getNombre()==claseSelec:
                LTTurno=unaClase.getTurnos()
                for turno in LTTurno:
                    self.turno.addItem(turno.getHorario())
                break

    def cancelarOp(self):
        cancela=QMessageBox.question(self, "Aviso", "Desea cancelar la operacion?",QMessageBox.No|QMessageBox.Yes, QMessageBox.Yes )
        if cancela==QMessageBox.Yes:
            self.close()

    def confirmarDatos(self):
        
        if self.controlCompleto(): 
            confirma=QMessageBox.question(self, "Aviso", "Desea guardar los datos ingresados para el nuevo socio?",QMessageBox.No|QMessageBox.Yes, QMessageBox.Yes )
            
            if confirma==QMessageBox.Yes:
                #nombre, dni, email, tel, domicilio, sexo, foto, antMed
                datos=[self.nombre.text(), self.dni.text(), self.email.text(), self.telefono.text(), self.domicilio.text() ] #falta antecedentes medcicos
                if self.masculino.isChecked():
                    datos.append('M')
                else:
                    datos.append('F')
                for clase in self.clases:
                    if clase.getNombre()==self.actividad.currentText():
                        
                        unaClase=clase
                        unTurno=None
                        
                        if self.actividad.currentText()!='Complemento':
                            for turno in clase.getTurnos():
                                if turno.getHorario()==self.turno.currentText():
                                    unTurno=turno
                                    break
                        break
                datos.append('') 
                datos.append('')
                datos.append(unaClase)
                datos.append(unTurno)
                if CTRLregistrarSocio.registrarsocio(self, datos):
                    self.notificarExito(True)
                else:
                    self.notificarExito(False)

    def notificarExito(self,exito):
        if exito:
            resultado='Nuevo socio registrado correctamente'
            
        else:
            resultado='No se pudo registrar al nuevo socio'
            
        QMessageBox.about(self, "Aviso", resultado)
    
    def destroy(self):
        pass


        

CTRLregistrarSocio().ejecutar()



