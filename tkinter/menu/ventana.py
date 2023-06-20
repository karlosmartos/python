from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import platform
from screeninfo import get_monitors
import tkinter.font as tkFont
from tkinter import scrolledtext
import procesos as po
from os import path



class menu:

#-----------------------------------Funciones para proceso general-----------------------------------------------

    #tamaños de la pantalla dividido en la mitad y se ajuste a la pantalla de acuerdo al sistema operativo

    altura=0

    ancho=0

    campos = []

    titles = []

    nombresCampos = []

    machinepass = '' 

    opcionesMenu=["Seleccione una opcion"]

    envio = []

    # detectamos el sistema operativo para poder darle las dimensiones a la venta, de acuerdo a la pantalla 
    def detectarSO(self):

        sistema = platform.system()

        plataforma =  0

        if(sistema == "Windows"):

            plataforma = 1

        if(sistema == "Linux"):

            plataforma = 2

        if(sistema == "Darwin"):

            plataforma = 3

        return plataforma

    def detectarpantalla(self, Sistema):

        pantallas = get_monitors()
       
        if(Sistema == 1):

            self.altura = pantallas[0].height/2

            self.ancho = pantallas[0].width/2
        
        if(Sistema == 2):

            self.altura = pantallas[0].height/2

            self.ancho = pantallas[0].width/2

        if(Sistema == 3):

            self.altura = pantallas[0].height/2

            self.ancho = pantallas[0].width/2
    
# Funcion de captura de ruta del archivo con la llave encriptada

    def CapturarRuta(self):

        error = 0

        Confirmacion = messagebox.askyesno(
         message='¿Seguro Quiere Seleccionar otra Credencial?\n'+ 'Si selecciona otro documento y no es correcto, necesita volver a iniciar el sistema para que queden los valores por defecto'
        , title='Modificacion Credencial')

        if (Confirmacion == True):

            try:
                self.documento =  filedialog.askopenfilename()

                self.ubicacion.set(self.documento)

                self.machinepass = po.revelar(self.documento)

                self.ComboBox["values"] = po.recuperar_menu(self.opcionesMenu, self.machinepass)

                self.rutadefecto = self.documento

                self.bucarllavero.config(state='disable')

            except:

                error = 1
            
            finally:

                if(error == 1):

                    messagebox.showinfo(message="La credencial no es correcta volver a intentar", title= "ATENCION")
               
# Terminar Proceso de ejecucion de menu

    def ValidarSalida(self):

        Confirmacion = messagebox.askyesno(message='¿Seguro Quiere Salir?', title='Salir')

        if(Confirmacion == True):

            self.Esqueleto.destroy()
        


# Aqui ira validacion para realizar proceso de ejecucion

    def ValidarEjecucion(self):

        valorRuta = len(self.ubicacion.get())

        valorMenu = self.ComboBox.current()

        if(valorRuta != 0 and valorMenu !=0):

            try:

                self.machinepass =  po.revelar(self.rutadefecto)

                if(po.val_archivo(self.ComboBox.current(), self.machinepass) == 2):

                    self.Formularia()

                else:
                    messagebox.showinfo('Info.','La tarea solicitada se encuentra en ejecucion, favor intentar más tarde')

            except:

                messagebox.showerror(message='Su Key de acceso no es correcta, revisar ', title='Error')

        else:

            messagebox.showinfo('Revisar','Llave o opcion no seleccionados, Revisar')


#------------------------------Fin definiciones de funciones para procesos generales-----------------------------



#-----------------Codigo y funcionalidades para ventana de ejecucion de procesos---------------------------------

    def MenuPrincipaldefault(self):

        self.ubicacion.set(self.rutadefecto)

        self.ComboBox.current(0)


    def CloseViewHija(self):

        self.formulario.destroy()

        self.Esqueleto.destroy()


    def VolverMenuPrincipal(self):

        Confirmacion = messagebox.askyesno(message='¿Seguro Quiere Volver al Menu?', title='Atencio')

        if(Confirmacion == True):

            self.formulario.destroy()

            self.campos.clear()

            self.titles.clear()

            self.nombresCampos.clear()

            self.envio.clear()

            self.MenuPrincipaldefault()

            self.Esqueleto.deiconify()

            self.Esqueleto.iconbitmap('image/icon/icono.ico')

            self.logo = PhotoImage(file = 'image/logos/logo-entel.png')

            Label(self.Esqueleto, bg='white' ,image= self.logo).place(x= 40, y=40)

    def CerrarAmbasVentanas(self):

        Confirmacion = messagebox.askyesno(message='¿Seguro Quiere Salir?', title='Salir')

        if(Confirmacion == True):

            self.formulario.destroy()

            self.Esqueleto.destroy()

            
    def RecuperarFormulario(self):
        
        Confirmacion = messagebox.askyesno(message='¿Seguro Que los datos son Correctos?', title='Atencio')

        if(Confirmacion == True):

            self.log.config(state='normal')

            for campo in self.campos:

                self.envio.append(campo.get())

                campo.config(state='disable')
            
            self.log.insert(INSERT, "Se Inicia el Procesamiento\n")

            self.log.insert(INSERT, "Tarea Ejecutandose, Favor espere hasta que este termine\n")

            try:

                respuestaServidor = po.ejecucion(self.ComboBox.current(), self.envio, self.machinepass)

                self.log.insert(INSERT,"Respuesta del servidor:\n")

                self.log.insert(INSERT, respuestaServidor+"\n")

                self.log.insert(INSERT,"Se ha bloqueado el formulario, mientras la tarea es ejecutada, favor regresar al menu principal, en caso de un error volver a intentarlo desde el menu principal.")
            
                self.log.config(state='disable')

                self.captura.config(state='disable')

                self.envio.clear()

            except:

                messagebox.showerror(message='Problema en la conexion o fallo en la ejecucion del proceso', title='Error')

            finally:

                 self.log.config(state='disable')

        else:

            for reset in self.campos:

                reset.delete(0,'end')


    def AgregarCampos(self):

        self.titles = po.recuperar_campos_Formulario(self.titles, self.ComboBox.current(), self.machinepass)

        for element in self.titles:

            self.nombresCampos.append(Label(self.Marco, bg='gray83' ,text=element, font='bold' ))

            self.campos.append(Entry(self.Marco,bg="white" ,width=30,borderwidth=2, relief="groove"))

    def Formularia(self):

        self.formulario = Toplevel(self.Esqueleto)

        self.Esqueleto.withdraw()

        self.formulario.title('Informacion a enviar para Procesar')

        self.formulario.config(bg='white')

        self.formulario.protocol("WM_DELETE_WINDOW", self.CloseViewHija)

        # self.operationSystem = self.detectarSO()

        # self.detectarpantalla(self.operationSystem)

        self.formulario.geometry(""+str(int(self.ancho-60))+"x"+str(int(self.altura+80))+"")

        self.formulario.resizable(width=0, height=0)

        self.formulario.iconbitmap('image/icon/icono.ico')

        self.logo = PhotoImage(file = 'image/logos/logo-entel.png')

        Label(self.formulario, bg='white' ,image= self.logo).place(x= 20, y=20)

        self.fuente = tkFont.Font(family ='Helvetica', size= 20)

        Label(self.formulario, bg='white' ,text= self.ComboBox.get(),font= self.fuente).grid(column = 0 , row =0 , padx=200 , pady= 40)

        self.Marco = Frame(self.formulario , bg = "gray83",borderwidth=2 ,relief="groove")

        self.Marco.config(width=600, height=300)

        self.Marco.place(x= 200, y= 80)

        self.AgregarCampos()

        contador = 0

        x1=20

        x2=250

        y=20

        y2 = 25

        for contenedor in self.campos:

            self.nombresCampos[contador].place(x = x1, y = y)

            contenedor.place(x= x2 , y = y2 )

            y = y+55
            y2 = y2+55
            contador = contador +1
            
        #-------------- se crea el frame y canvas con scrollbar de formulario----------------------------------------------
        # se Cambia este  codigo por un frame simple y una ventana de log, ya que se confirma que el maximo de valores 
        # sera de 5 campos maximo por tarea

        # self.framePadre1 = Frame(self.formulario,bg='blue', borderwidth=2 ,relief="groove" )

        # self.framePadre1.place(x= 220, y= 100)

        # self.barraDesplazamiento= Scrollbar(self.framePadre1)

        # self.barraDesplazamiento.pack(side=RIGHT,fill=Y)

        # self.Lienzo = Canvas(self.framePadre1,width=400, height= 300, bg= "white", yscrollcommand= self.barraDesplazamiento.set)

        # self.frameHijo= Frame(self.Lienzo)

        # self.Lienzo.pack(fill=BOTH)

        # self.Lienzo.create_window(0,0,window=self.frameHijo,anchor='nw')

        # self.barraDesplazamiento.config(command= self.Lienzo.yview)

        # self.AgregarCampos()

        # contador = 0

        # for elemento in self.campos:

        #     self.nombresCampos[contador].pack(fill="x")

        #     elemento.pack()

        #     contador = contador+1

        # self.framePadre1.update()

        # self.Lienzo.config(scrollregion= self.Lienzo.bbox("all"))

#------------------------- fin codigo de formulario con scrollbar---------------------------------------------------


        self.captura= Button(self.formulario, text='Ejecutar', command=self.RecuperarFormulario)

        self.captura.place(x=300, y = 580)

        self.regresar = Button(self.formulario,text='Volver a Menu',command=self.VolverMenuPrincipal)

        self.regresar.place(x=400, y =580)

        self.salir = Button(self.formulario, text='Salir', command= self.CerrarAmbasVentanas)

        self.salir.place(x= 550, y = 580)

        self.log = scrolledtext.ScrolledText(self.formulario, width = 72, height = 10,borderwidth=2 ,relief="groove", bg="gray83",state='disable')

        self.log.place(x= 200, y = 400)

        equipo = Label(self.formulario, text="By Team SDD", borderwidth=2, relief="groove", bg = "white")

        equipo.place(x= 10 , y = 595)

#-----------------------------------------Fin Codigo Ventana de Procesos------------------------------------------

#----------------------------------------Codigo Ventana Principal Menu--------------------------------------------

#Constructor del objeto Ventana Principal
# cambiar ruta por defecto donde quedara la clave de la maquina 
    def __init__(self):

        self.Esqueleto = Tk()

        self.ubicacion = StringVar()

        self.nombreArchivo = "Key.bin"

        self.rutadefecto = path.abspath(self.nombreArchivo)

        self.ubicacion.set(self.rutadefecto)   

        self.Esqueleto.title("Facturación BSCS") 

        self.Esqueleto.config(bg='white')

        self.Esqueleto.resizable(width=0, height=0)

        # self.So = self.detectarSO()

        # self.detectarpantalla(self.So)

        self.altura = 540

        self.ancho = 1030

        self.Esqueleto.geometry(""+str(int(self.ancho -350))+"x"+str(int(self.altura/2 + 20))+"")

        self.Esqueleto.iconbitmap('image/icon/icono.ico')

        self.logo = PhotoImage(file = 'image/logos/logo-entel.png')

        Label(self.Esqueleto, bg='white' ,image= self.logo).place(x= 40, y=40)

        self.fuente = tkFont.Font(family ='Helvetica', size= 20)

        titulo=Label(self.Esqueleto, bg= 'white' ,text="Procesos", font= self.fuente)

        titulo.grid(column = 0 , row =0 , padx=250 , pady= 50)

        Label(self.Esqueleto, bg = 'white', text='Credencial').place(x=150, y = 130 )

        self.llavero = Entry(self.Esqueleto, width= 50, text = self.ubicacion,borderwidth=2, relief="groove",state='disable' )

        self.llavero.place(x= 220, y= 130)

        self.bucarllavero = Button(self.Esqueleto,text="Modificar Credencial",borderwidth=2, relief="groove", command= self.CapturarRuta)

        self.bucarllavero.place(x= 220, y= 160)

        self.ComboBox = ttk.Combobox(self.Esqueleto,state="readonly", width= 40)

        Label(self.Esqueleto, bg= 'white', text='Seleccione una tarea').place(x=100, y= 200) # x= 150, y= 200  se cambia por el valor original x=580, y = 123 

        self.ComboBox.place(x=220, y= 200) # 220, y= 220  se cambia por  el valor original x= 615, y = 160

        try:

            self.machinepass = po.revelar(self.rutadefecto)

            self.ComboBox["values"] = po.recuperar_menu(self.opcionesMenu, self.machinepass)

            self.ComboBox.current(0)

            self.bucarllavero.config(state='disable')

        except:

            messagebox.showerror(message="Su credencial esta descontinuada o presenta errores internos, favor seleccionar otra", title="ERROR")

            self.ComboBox["values"] = self.opcionesMenu

            self.ComboBox.current(0)


        finally:

            self.Ejecutar = Button(self.Esqueleto, text='Ejecutar Tarea',borderwidth=2, relief="groove", command=self.ValidarEjecucion)

            self.Salir = Button(self.Esqueleto, text='Salir',borderwidth=2, relief="groove" , command= self.ValidarSalida)

            self.Ejecutar.place(x=500, y= 200) #(x=380, y= 200 -> se cambia por (x=780, y = 160)

            self.Salir.place(x=600 ,y = 200 ) # x= 220, y= 200-> se cambia por (x=880 ,y = 160 )

            self.equipo = Label(self.Esqueleto, text="By Team SDD", borderwidth=2, relief="groove", bg = "white")

            self.equipo.place(x= 10 , y = 258)

            self.Esqueleto.mainloop()

#----------------------------------Fin codigo Ventana Principal menu-----------------------------------------------