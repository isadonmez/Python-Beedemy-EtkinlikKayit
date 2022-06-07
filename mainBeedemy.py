# -*- coding: utf-8 -*-
"""
Created on Mon May 17 16:44:17 2021

@author: Admin
"""

#-------------------------------  Kütüphane ---------------------------------#
#----------------------------------------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from kampKaydiUI import *


#--------------------------- Uygulama Oluştur -------------------------------#
#----------------------------------------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()




#--------------------------- Veritabanı Oluştur -----------------------------#
#----------------------------------------------------------------------------#
##############################################################################

import sqlite3
global curs
global conn
conn=sqlite3.connect('veritabani3.db ')
curs=conn.cursor()
sorguCreTblkampKaydi=("CREATE TABLE IF NOT EXISTS kampKaydivt(              \
                    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   \
                    Adiniz TEXT NOT NULL ,                           \
                    Soyadiz TEXT NOT NULL,                           \
                    TCNo TEXT NOT NULL UNIQUE,                       \
                    KampinAdi TEXT NOT NULL,                         \
                    Cinsiyet TEXT NOT NULL,                          \
                    DTarihi TEXT NOT NULL,                           \
                    Dekont TEXT NOT NULL,                            \
                    OdenenKisi TEXT NOT NULL,                        \
                    HesKodu TEXT NOT NULL)")

curs.execute(sorguCreTblkampKaydi)
conn.commit()
##############################################################################



#----------------------------  Kaydet Butonu  -------------------------------#
#----------------------------------------------------------------------------#
##############################################################################
def KAYDET():
     _lneAd=ui.lneAd.text()
     _lneSoyad=ui.lneSoyad.text()
     _lneTC=ui.lneTC.text()
     _cmbKampAdi=ui.cmbKampAdi.currentText()
     _cmbCinsiyet=ui.cmbCinsiyet.currentText()
     _cwDTarihi=ui.cwDTarihi.selectedDate().toString(QtCore.Qt.ISODate)

     if ui.chkOdeme.isChecked():
         _chkOdeme="Odendi"
     else:
         _chkOdeme="Odenmedi"
         
     _cmbOdenenKisi=ui.cmbOdenenKisi.currentText() 
     _lneHesKodu=ui.lneHesKodu.text()

     curs.execute("INSERT INTO kampKaydivt \
                     (Adiniz,Soyadiz,TCNo,KampinAdi,Cinsiyet,DTarihi,Dekont,ODenenKisi,HesKodu)\
                       VALUES (?,?,?,?,?,?,?,?,?)",\
                       (_lneAd,_lneSoyad,_lneTC,_cmbKampAdi,_cmbCinsiyet,\
                        _cwDTarihi,_chkOdeme,_cmbOdenenKisi,_lneHesKodu))
     conn.commit()
     ui.lneAd.clear()
     ui.lneSoyad.clear()
     ui.lneTC.clear()
     ui.cmbCinsiyet.setCurrentIndex(-1)
     ui.chkOdeme.setChecked(False)
     ui.cmbOdenenKisi.setCurrentIndex(-1)
     ui.lneHesKodu.clear()

    #LISTELE()
     ui.statusbar.showMessage("Kayit islemi basariyla gerceklesti...",10000)
##############################################################################




#-------------------------------  Listele -----------------------------------#
#----------------------------------------------------------------------------#
##############################################################################
def LISTELE():
    ui.tblwkampBilgi.clear()
    ui.tblwkampBilgi.setHorizontalHeaderLabels(('No','Kampin Adi','Ad', 'Soyad', 'TC No', \
                                                  'Cinsiyet', 'Dogum Tarihi','Dekont',  \
                                                   'OdenenKisi', 'Hes Kodu'))
    ui.tblwkampBilgi.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT * FROM kampKaydivt")
    for satirIndeks,satirVeri in enumerate(curs):
        for sutunIndeks,sutunVeri in enumerate(satirVeri):
            ui.tblwkampBilgi.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    
    ui.lneAd.clear()
    ui.lneSoyad.clear()
    ui.lneTC.clear()
    ui.cmbCinsiyet.setCurrentIndex(-1)
    ui.chkOdeme.setChecked(False)
    ui.cmbOdenenKisi.setCurrentIndex(-1)
    ui.lneHesKodu.clear()

    
#LISTELE()
##############################################################################


#-------------------------------   Sil  -------------------------------------#
#----------------------------------------------------------------------------#
def SIL():
     cevap=QMessageBox.question(penAna, "Kayıt Sil", "Kaydı silmek istediginize emin misiniz?", \
                            QMessageBox.Yes | QMessageBox.No)
     if cevap==QMessageBox.Yes:
         secili=ui.tblwkampBilgi.selectedItems()
         silinecek=secili[4].text()
         try:
             curs.execute("DELETE FROM kampKaydivt WHERE TCNo='%s'" %(silinecek))
             conn.commit()
             #LISTELE()
             ui.statusbar.showMessage("Kayit silme islemi basariyla gerceklesti...",10000)
             ui.lneAd.clear()
             ui.lneSoyad.clear()
             ui.lneTC.clear()
             ui.cmbCinsiyet.setCurrentIndex(-1)
             ui.chkOdeme.setChecked(False)
             ui.cmbOdenenKisi.setCurrentIndex(-1)
             ui.lneHesKodu.clear()
      
         except Exception as Hata:
            ui.statusbar.showMessage("Söyle bir hata ile karsilasildi:"+str(Hata))
     else:
        ui.statusbar.showMessage("Silme islemi iptal edildi.",10000)
        
        ui.lneAd.clear()
        ui.lneSoyad.clear()
        ui.lneTC.clear()
        ui.cmbCinsiyet.setCurrentIndex(-1)
        ui.chkOdeme.setChecked(False)
        ui.cmbOdenenKisi.setCurrentIndex(-1)
        ui.lneHesKodu.clear()



#-------------------------------   Arama Butonu -----------------------------#
#----------------------------------------------------------------------------#
##############################################################################
def ARA():
    aranan1=ui.lneTC.text()
    aranan2=ui.lneHesKodu.text()
    #aranan2=ui.lneAd.text()
    #aranan3=ui.lneSoyad.text()
    curs.execute("SELECT * FROM kampKaydivt WHERE TCNo=? OR HesKodu=?", \
                 (aranan1,aranan2))
    
    conn.commit()
    ui.tblwkampBilgi.clear()
    for satirIndeks,satirVeri in enumerate(curs):
        for sutunIndeks,sutunVeri in enumerate(satirVeri):
            ui.tblwkampBilgi.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
   

##############################################################################



#-------------------------------  Doldur(Güncelle)---------------------------#
#----------------------------------------------------------------------------#
##############################################################################
def DOLDUR():
     secili=ui.tblwkampBilgi.selectedItems()
     
     ui.cmbKampAdi.setCurrentText(secili[1].text())
     ui.lneAd.setText(secili[2].text())
     ui.lneSoyad.setText(secili[3].text())
     ui.lneTC.setText(secili[4].text())
     ui.cmbCinsiyet.setCurrentText(secili[5].text())
     
     yil=int(secili[6].text()[0:4])
     ay=int(secili[6].text()[5:7])
     gun=int(secili[6].text()[8:10])
     ui.cwDTarihi.setSelectedDate(QtCore.QDate(yil,ay,gun))

     if secili[7].text()=="Odendi":
         ui.chkOdeme.setChecked(True)
     else:
         ui.chkOdeme.setChecked(False)
 
     ui.cmbOdenenKisi.setCurrentText(secili[8].text())
     ui.lneHesKodu.setText(secili[9].text())     
##############################################################################


#------------------------------- Güncelle --- -------------------------------#
#----------------------------------------------------------------------------#

def GUNCELLE():
      cevap=QMessageBox.question(penAna, "Kayıt Güncelleme", "Kaydı güncellemek istediginize emin misiniz?", \
                            QMessageBox.Yes | QMessageBox.No)
      if cevap==QMessageBox.Yes:
           try:
              secili=ui.tblwkampBilgi.selectedItems()
              _Id=int(secili[0].text())
              _cmbKampAdi=ui.cmbKampAdi.currentText()
              _lneAd=ui.lneAd.text()
              _lneSoyad=ui.lneSoyad.text()
              _lneTC=ui.lneTC.text()              
              _cmbCinsiyet=ui.cmbCinsiyet.currentText()
              _cwDTarihi=ui.cwDTarihi.selectedDate().toString(QtCore.Qt.ISODate)
             
              if ui.chkOdeme.isChecked():
                  _chkOdeme="Odendi"                   
              else:
                  _chkOdeme="Odenmedi" 
                   
              _cmbOdenenKisi=ui.cmbOdenenKisi.currentText()
              _lneHesKodu=ui.lneHesKodu.text()             
                
              curs.execute("UPDATE kampKaydivt SET Adiniz=?, Soyadiz=?, TCNo=?, KampinAdi=?, \
                           Cinsiyet=?, DTarihi=?, \
                           Dekont=?, ODenenKisi=?, HesKodu=? WHERE Id=?", \
                          (_lneAd,_lneSoyad,_lneTC,_cmbKampAdi,_cmbCinsiyet,\
                           _cwDTarihi,_chkOdeme,_cmbOdenenKisi,_lneHesKodu,_Id))
              ui.statusbar.showMessage("Güncelleme başarılı",10000)  
           except Exception as Hata:
               ui.statusbar.showMessage("Şöyle bir hata meydana geldi" + str(Hata))
            
         
      else:
          ui.statusbar.showMessage("Güncelleme iptal edildi",10000)
          
      ui.lneAd.clear()
      ui.lneSoyad.clear()
      ui.lneTC.clear()
      ui.cmbCinsiyet.setCurrentIndex(-1)
      ui.chkOdeme.setChecked(False)
      ui.cmbOdenenKisi.setCurrentIndex(-1)
      ui.lneHesKodu.clear()
      conn.commit()
      #LISTELE()
       
      
#--> Devam
#------------------------------ Hakkında----- -------------------------------#
#----------------------------------------------------------------------------#
def HAKKINDA():
    penHakkinda.show()  



#-----------------------------   Sinyal-Slot   ------------------------------#
#----------------------------------------------------------------------------#
ui.btnKaydet.clicked.connect(KAYDET)
ui.btnAra.clicked.connect(ARA)
ui.btnGuncelle.clicked.connect(GUNCELLE)
ui.btnListele.clicked.connect(LISTELE)
ui.tblwkampBilgi.itemSelectionChanged.connect(DOLDUR)
ui.btnSil.clicked.connect(SIL)


sys.exit(Uygulama.exec_())
   
    


