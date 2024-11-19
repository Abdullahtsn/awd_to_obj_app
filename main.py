
import os
import struct
import sys
from pygame import mixer as pymix   #sadece mixer kısmını aktarıp bunu pymix adı altında kullanmak için.
pymix.init()

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from design import Ui_MainWindow  
from developer_design import Ui_Form   

from pyawd.PyAwdLogger import logger
from pyawd.awd import AWDDocument
from pyawd.awd.blocks.MeshInstanceBlock import MeshInstanceBlock
from pyawd.awd.types.streams.FaceIndexStream import FaceIndexStream
from pyawd.awd.types.streams.UVCoordinatesStream import UVCoordinatesStream
from pyawd.awd.types.streams.VertexPositionsStream import VertexPositionsStream



if getattr(sys,'frozen', False):        
    os.chdir(sys._MEIPASS)
else:                       
    os.chdir('.')

def build_obj(block):
    vertices = []
    normals = []  
    uvs = []
    faces = []
    global f_offset
    for mesh in block.sub_meshes:
        for geo in mesh.geometry_data_blocks:
            if isinstance(geo, VertexPositionsStream):
                vertices.extend([f"v {vertex[0]} {vertex[1]} {vertex[2]}" for vertex in geo.vertices])
            elif isinstance(geo, UVCoordinatesStream):
                uvs.extend([f"vt {coordinate[0]} {1.0 - coordinate[1]}" for coordinate in geo.coordinates])
            elif isinstance(geo, FaceIndexStream):
                faces.extend([f"f {face[0] + f_offset}/{face[0] + f_offset} {face[1] + f_offset}/{face[1] + f_offset} {face[2] + f_offset}/{face[2] + f_offset}" for face in geo.faces])
    f_offset += len(vertices)
    return vertices, normals, uvs, faces

def convert_to_obj(path_to_input_file):     #awdnin tam yolunu gönderiyoruz
    global f_offset
    global output_string
    f_offset = 1
    file = open(path_to_input_file, 'rb')
    document = AWDDocument.decode(file)
    filename = os.path.splitext(os.path.basename(file.name))[0]
    output_string = f""
    for block_id in document.blocks:
        header, block = document.blocks[block_id]
        if isinstance(block, MeshInstanceBlock):
            block_body = document.blocks[block.mesh_block_id][1]
            if isinstance(block_body, str):
                logger.error(f"Could not parse mesh '{filename}' because of this error: {block_body}")
                raise RuntimeError()
            lookup_name = block.scene_header.lookup_name
            output_string += f"o {lookup_name}\n"
            vertices, normals, uvs, faces = build_obj(block_body)
            output_string += "\n".join(vertices) + "\n"
            output_string += "\n".join(normals) + "\n"  
            output_string += "\n".join(uvs) + "\n"
            output_string += "\n".join(faces) + "\n"
    pass


def save_to_obj(awd_file, obj_save):        #hem awdnin tam yolunu hemde kaydedilcek dizini gönderiyoruz.
    awd_convert_obj = os.path.basename(awd_file)        #burada awd dosyasını tam dizinden ayrıştırıp sadece dosya adı kısmını alıyoruz.
    awd_extend = awd_convert_obj.replace('.awd','.obj')     #tam dosya adının uzantısını değiştirip verileri ona uygun yazıyoruz.
    with open(os.path.join(obj_save, awd_extend), 'w') as o:
        o.write(output_string)
    


def one_awd_convert_to_obj(awd_file_list, obj_save):    
    for awd_file in awd_file_list:  
        convert_to_obj(awd_file)    #buraya awdnin tam yolunu gönderiyoruz
        save_to_obj(awd_file, obj_save)  

'''def folder_awd_convert():   #klasörlü dönüştürme. burayı kullanmıyorum not olarak kalsın diye yazılı. (terminalden çalıştırıp klasör hedefi verirsen çalışmalı burası.)
    awd_path, obj_path = sys.argv[1], sys.argv[2]   #terminaldeki ikinci ve üçüncü kelime
    failed_files = []
    for cur_file in os.listdir(awd_path):
        if cur_file.endswith(".awd"):
            logger.info(f"Convert {cur_file}")
            try:
                convert_to_obj(awd_path + "/" + cur_file)
                save_to_obj(obj_path + "/" + cur_file.replace(".awd", ".obj"))
            except (RuntimeError, struct.error, KeyError, AttributeError):
                failed_files.append(cur_file)
    logger.info(f"Failed files: {failed_files}")'''



#one_awd_convert()       #tek hedefli dönüştürme(çok hedef seçebilmeye göre uyarlandı.)
#folder_awd_convert()    #bu fonksiyonun içindeki sys.argv[1 ve 2] 'nin temsil ettiği terminalde girilen ikinci ve üçüncü kelime. eğer konsoldan klasör hedefi verip içindeki tüm awdleri dönüştürüceksen yukarıyı yorum satırı yap burayı aç.
    
class MsgBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.close_icon = QtGui.QPixmap(os.path.join('icon','close2.png'))
        self.not_file_icon = QtGui.QPixmap(os.path.join('icon','not_file.png'))
        self.info_icon = QtGui.QPixmap(os.path.join('icon','info.png'))
        self.ok_icon = QtGui.QPixmap(os.path.join('icon','ok.png'))
        self.warning_icon = QtGui.QPixmap(os.path.join('icon','warning.png'))
        self.succes_icon = QtGui.QPixmap(os.path.join('icon','succes.png'))
        self.retry_icon = QtGui.QPixmap(os.path.join('icon','retry.png'))
        self.setStyleSheet('color:white ; background-color:black')
        self.setWindowIcon(QtGui.QIcon(self.info_icon))     #açılan tüm pencerelerin titlebar iconu sabit olcağı için burda bir defa değiştirdik. duruma göre değiştirmek gerekirse aşağıdaki fonksiyondan parametre alarak belirleyebilirsin.
        self.setStandardButtons(self.Ok)    # bunu dışardan parametre olarak birden fazla duruma göre buton ekleyebiliriz ama bu uygulama için her koşulda sadece ok butonu olcağı için gerek görülmedi.
        #self.button(self.Ok).setStyleSheet('padding-right:90px')   #messageboxun içindeki ok botununu ortalama. grid layout şeklinde yerleştirildiği için padding ile sağdan boşluk bırakarak ortalamış gibi gösterebiliyoruz.
        self.button(self.Ok).setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    def messagebox_edit(self, title, text, icon):     #her mesaj kutusunu ayrı ayrı oluşturmak yerine bir mesaj kutusunu dışardan gelcek verilerle güncelleyip bellek kullanımını azaltıcaz.
        self.setWindowTitle(title)
        self.setText(text)
        self.setIconPixmap(icon)
        self.exec_()

        '''for i in self.children():        #qmessageboxun içindeki widgetleri listeleme
            print(i)'''

    def messagebox_1(self, directory):
        self.messagebox_edit('Successful !',f'\n\nAwd extension converted to obj extension.\nDirectory: {directory}', self.succes_icon)
    
    def messagebox_2(self):
        self.messagebox_edit('Not found !','\n\nAwd file not selected.', self.not_file_icon)

    def messagebox_3(self):
        self.messagebox_edit('Select save directory !','\n\nThe directory for the obj file to\nbe saved has not been selected.', self.warning_icon)

class Developer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.github = self.ui.label_github.text()
        self.gmail = self.ui.label_gmail.text()
        self.pano = QtWidgets.QApplication.clipboard()      #kullanıcının  panoya ulaşması oraya bişeyler kopyalayıp yada panodaki kopyalı olanı yapıştırabilmesi için pyqtnin kendi fonksiyonu.

        self.ui.pushButton_close.clicked.connect(self.window().close)
        self.ui.pushButton_github.clicked.connect(self.button_github)
        self.ui.pushButton_gmail.clicked.connect(self.button_gmail)
        self.load_icon()

    def load_icon(self):
        icon_size_button = 40,40
        self.ui.pushButton_close.setIcon(QtGui.QIcon(os.path.join('icon','close.png'))) 
        self.ui.pushButton_github.setIcon(QtGui.QIcon(os.path.join('icon','copy.png'))) 
        self.ui.pushButton_gmail.setIcon(QtGui.QIcon(os.path.join('icon','copy.png'))) 
        
        self.ui.pushButton_close.setIconSize(QtCore.QSize(icon_size_button[0],icon_size_button[1]))
        self.ui.pushButton_github.setIconSize(QtCore.QSize(icon_size_button[0],icon_size_button[1]))
        self.ui.pushButton_gmail.setIconSize(QtCore.QSize(icon_size_button[0],icon_size_button[1]))


    def button_github(self):
        self.pano.setText(self.github)      #butona tıklanınca panoya kopyalaması için

    def button_gmail(self):
        self.pano.setText(self.gmail)       #butona tıklanınca panoya kopyalaması için



class Sounds:
    def __init__(self):
        self.sound_1 = pymix.Sound(os.path.join('sound','sound_1.mp3'))
        self.sound_2 = pymix.Sound(os.path.join('sound','sound_2.mp3'))
        self.sound_1.set_volume(0.25)
        self.sound_2.set_volume(0.25)
    
    def sound_1_play(self):
        self.sound_1.play()

    def sound_2_play(self):
        self.sound_2.play()


class ConvertApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ConvertApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sounds = Sounds()
        self.sound = True
        self.msgbox = MsgBox()
        self.developer_window = Developer()
        self.awd_directory = None   
        self.obj_directory = None

        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join('icon','icon.ico'))))

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)   #varsayılan pencereyi göstermemesi için.        
        
        self.ui.toolButton_close.clicked.connect(self.window().close)
        self.ui.toolButton_minimize.clicked.connect(self.window().showMinimized)

        #aşağıdaki 3 fonksiyon sırasıyla o buton için tıklama, tıklı haldeyken fare hareketi, ve tıklamayı bırakma olaylarını işliyor.
        #pyqt nin hazır fonksiyonlarını eşitliğin sağ tarafındaki kendi oluşturduğumuz fonksiyonlara aktarıyoruz.(sadece move butonuna tıklanınca pencere hareketi için özelleştirme.)
        self.ui.toolButton_move.mousePressEvent = self.move_button_pressed_event
        self.ui.toolButton_move.mouseMoveEvent = self.move_button_move_event
        self.ui.toolButton_move.mouseReleaseEvent = self.move_button_release_event
        #self.ui.toolButton_move.setCursor(QtCore.Qt.BlankCursor)      #bu widgete gelince fareyi görünmez yapıyor. biz sadece tıklanıldığında görünmez yapması için yukardaki fonksiyonlara ekliycez bunu
        

        self.ui.toolButton_sound.clicked.connect(self.sound_button)
        self.ui.toolButton_developer.clicked.connect(self.developer_button)
        self.ui.pushButton_selectfile.clicked.connect(self.select_file)
        self.ui.pushButton_save.clicked.connect(self.save_file)
        self.ui.pushButton_start.clicked.connect(self.start_convert)
        
        self.icon_load()
        

    def icon_load(self):
        icon_size_titlebar = 30,30
        icon_size_button = 40,40

        icon_pixmap = QtGui.QPixmap(os.path.join('icon','icon.png'))
        self.ui.label_icon.setPixmap(icon_pixmap.scaled(icon_size_titlebar[0]-3, icon_size_titlebar[1]-3 ))     #qlabele ikonu eklerken butonlardaki gibi set icon diyerek ekleyemiyoruz. o yüzden setpixmap diye icon eklememiz gerekiyor labellere. ölçülerinide scaled yöntemiyle ayarlıyoruz.

        self.ui.toolButton_close.setIcon(QtGui.QIcon(os.path.join('icon','close.png')))
        self.ui.toolButton_minimize.setIcon(QtGui.QIcon(os.path.join('icon','minimize.png')))
        self.ui.toolButton_move.setIcon(QtGui.QIcon(os.path.join('icon','move.png')))
        self.sound_on_icon = QtGui.QIcon(os.path.join('icon','sound_on.png'))
        self.sound_off_icon = QtGui.QIcon(os.path.join('icon','sound_off.png'))
        self.ui.toolButton_sound.setIcon(self.sound_on_icon)        #ses düğmesinde icon sürekli tıklanıcağı için tekrar tekrar yüklemesin diye yukarda ayrı değişkenlerde tanımladık.
        self.ui.toolButton_developer.setIcon(QtGui.QIcon(os.path.join('icon','developer.png')))
        self.ui.pushButton_selectfile.setIcon(QtGui.QIcon(os.path.join('icon','select.png')))
        self.ui.pushButton_save.setIcon(QtGui.QIcon(os.path.join('icon','save.png')))
        self.ui.pushButton_start.setIcon(QtGui.QIcon(os.path.join('icon','start.png'))) 
        
        self.ui.toolButton_close.setIconSize(QtCore.QSize(icon_size_titlebar[0],icon_size_titlebar[1]))
        self.ui.toolButton_minimize.setIconSize(QtCore.QSize(icon_size_titlebar[0],icon_size_titlebar[1]))
        self.ui.toolButton_move.setIconSize(QtCore.QSize(icon_size_titlebar[0],icon_size_titlebar[1]))
        self.ui.toolButton_sound.setIconSize(QtCore.QSize(icon_size_titlebar[0],icon_size_titlebar[1]))
        self.ui.toolButton_developer.setIconSize(QtCore.QSize(icon_size_titlebar[0],icon_size_titlebar[1]))
        self.ui.pushButton_selectfile.setIconSize(QtCore.QSize(icon_size_button[0],icon_size_button[1]))
        self.ui.pushButton_save.setIconSize(QtCore.QSize(icon_size_button[0],icon_size_button[1]))
        self.ui.pushButton_start.setIconSize(QtCore.QSize(icon_size_button[0],icon_size_button[1]))

    
    

    def move_button_pressed_event(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.initial_pos = event.pos()
        #super().mousePressEvent(event)     #bu şekilde yapınca designerde tanımladığım renklendirme olayı çalışmıyordu. 
        #burda tıklanınca bizim yaptığımız olay gerçekleşince önceki diğer işlevlerin devam etmesi için superin içine aşağıdaki şekilde bu nesneyi verdik. 
        #bu tool button için sürükleme ve bırakma olaylarının superlerinede ekledik bunu.
        #kısacası önceki işlevin silinmemesini ve devam etmesini istiyorsak superi kullanıyoruz.
        super(QtWidgets.QToolButton, self.ui.toolButton_move).mousePressEvent(event)
        event.accept()

    def move_button_move_event(self,event):
        self.setCursor(QtCore.Qt.BlankCursor)       #move tuşuna basılıyken farenin görünmez olmasını sağlıyor.
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super(QtWidgets.QToolButton, self.ui.toolButton_move).mouseMoveEvent(event)
        event.accept()

    def move_button_release_event(self, event):
        self.unsetCursor()          #farenin tuşu bırakılınca cursor ayarını kaldırıp eski haline getiriyor.
        self.initial_pos = None 
        super(QtWidgets.QToolButton, self.ui.toolButton_move).mouseReleaseEvent(event)
        event.accept()


    def sound_button(self):
        if self.sound:
            self.sound = False
            self.ui.toolButton_sound.setIcon(self.sound_off_icon) 
        else:
            self.sound = True
            self.ui.toolButton_sound.setIcon(self.sound_on_icon) 

    def developer_button(self):
        self.developer_window.show()


    def select_file(self):
        #kullanıcı birden fazla dosyayı dönüştürmek isterse diye liste olarak seçmesine izin verdim. eğer tek dosya seçmesini istersen getopenfilename olarak değiştir.
        directory = QtWidgets.QFileDialog.getOpenFileNames(self, caption='SELECT AWD FILE', filter = ('*.awd') )     #caption = dosya seçme penceresindeki başlık, filter=seçilecek dosyaları görüntülerken görüntülenicek uzantılar(burda sadece awdleri görüntülüyoruz başka dosya seçilmesin diye)
        if directory[0]:
            self.awd_directory = directory[0]
        else:
            pass
        
        #eğer butona tıklanma durumlarını kontrol ediceksen aşağıdaki butonları kontrol ediyor. benim işime yarayan sadece dosya konumu olduğu için gelen bilginin boş olup olmamasının kontrolünü sağladığım için buna gerek duymadım.
        '''dialog = QtWidgets.QFileDialog(self)         
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile) 
        dialog.setNameFilter("AWD Files (*.awd)") 
        if dialog.exec_() == QtWidgets.QFileDialog.Accepted: 
            selected_files = dialog.selectedFiles() 
            if selected_files: 
                self.awd_directory = selected_files[0] 
        else: 
            pass'''
            

    def save_file(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption='SAVE OBJ FILE')
        if directory:
            self.obj_directory = directory
        else:
            pass
            
    def start_convert(self):
        if self.awd_directory and self.obj_directory:
            one_awd_convert_to_obj(self.awd_directory, self.obj_directory)
            if self.sound:
                self.sounds.sound_1_play()
            self.msgbox.messagebox_1(self.obj_directory)
            self.awd_directory = None       #dönüşümden sonra awd dizinini sıfırlıyoruz. sonraki dönüşüm için başka bi dizin(başka bi awd dosyası) seçme uyarısı vermek için.
        
        elif self.awd_directory is None:
            if self.sound:
                self.sounds.sound_2_play()
            self.msgbox.messagebox_2()
            

        elif self.obj_directory is None:
            if self.sound:
                self.sounds.sound_2_play()
            self.msgbox.messagebox_3()
            
        
        
    #pyqt nin sabit fonksiyonları;

    '''def mousePressEvent(self, event):   #farenin basma olayları
        pass
        
    def mouseMoveEvent(self, event):     #farenin basılı tutarkenki hareket olayları
        pass
    
    def mouseReleaseEvent(self, event):    #farenin basılmasını bırakma olayları
        pass'''


    def closeEvent(self, event):            #uygulama kapanırkenki olaylar
        self.developer_window.close()       #ana pencereyi kapatınca eğer developer kısmı açıksa o pencere açık kalıyordu. 
                                            #böyle yapınca ana pencereyi kapatırken diğer pencere açıksa onuda kapatarak programı düzgün sonlandırmak için yazıldı burası.

            
        

    
    
    



def app():
    app = QtWidgets.QApplication(sys.argv)
    win = ConvertApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app()
    


