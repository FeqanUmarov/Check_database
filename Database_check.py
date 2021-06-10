import arcpy
from arcpy import env
import os
class Check_Database():
    print("""Cografi verilenler bazasinin yoxlanilmasi sistemine xos gelmisiniz. Yoxlamaya baslamaq ucun yoxlama aparilacaq databazani
     ve xetalarin gonderileceyi bazanin yolunu daxil edin (Numune: r"D:\ArcGIS Pro_file\ArcGIS_File\Bazalar\Example.mdb\RAYON" Burada 'RAYON'
     datasetin adidir. Yeni laylarin yerlesdiyi yerin File Path tam daxil etmek lazimdir.) Inputlar verildikden sonra, 'checkdata'
     yazaraq noqte qoyduqda ona bagli olan metodlar gelecekdir. Yoxlama ucun istifade etdilen metodlar bunlardir: checkdata.check_feature(),
     checkdata.create_topology(),checkdata.border_parcel_check(),checkdata.quarter_building_check(),checkdata.check_field_value_full(),
     checkdata.check_atribute(), checkdata.delete_extra_layer(), checkdata.delete_empty_feature()""")
################## Inputlar alinir ######################
    while True:
        try:
            ######### Emeliyyat gedecek databaza daxil edilir ###########
            database = input("Verilenler bazasinin yolunu daxil et:")
            if database!="":
                break
            else:
                print("Bazanin yolunu daxil edin!")
                continue
        except:
            print("Bazanin yolu dogru gosterilmeyib!")

    while True:
        try:
            ######### Xeatalarin gonderileceyi baza daxil edilir ###########
            output = input("Xetalarin gonderileceyi bazani daxil et:")
            if output!="":
                break

            else:
                print("Xetalarin gonderileceyi yeri daxil edin!")
                continue

        except:
            print("Xetalarin gonderileceyi yer teyin edilmeyib!")

################## Inputlar alinir ######################
    env.workspace = database
    arcpy.env.overwriteOutput = True

    def __init__(self):
        
        self.about_app()

    def about_app(self):
        print("""Cografi verilenler bazasinin yoxlanilmasi sistemine xos gelmisiniz! "check_feature"-verilenler bazasinda olan laylarin adlarinin standarta uygun olmasini yoxla
        (eger laylarin adi standart olmasa diger proseslerde xetalarla qarsilasa bilerik) """)

    def check_feature(self):
        try:
        ########## Databazada olan laylarin standart olub olmamasi yoxlanilir ################
            self.fcList = arcpy.ListFeatureClasses()
            if "TORPAQ_TUM" not in self.fcList:
                print("TORPAQ_TUM layi yoxdur ve ya adi duzgun yazilmayib!")
            if "TIKILI_TUM" not in self.fcList:
                print("TIKILI_TUM layi yoxdur ve ya adi duzgun yazilmayib!")
            if "SEKTOR" not in self.fcList:
                print("SEKTOR layi yoxdur ve ya adi duzgun yazilmayib!")
            if "QUARTER" not in self.fcList:
                print("QUARTER layi yoxdur ve ya adi duzgun yazilmayib!")
            if "Noqteler" not in self.fcList:
                print("Noqteler layi yoxdur ve ya adi duzgun yazilmayib!")
            if "KOMEKCI" not in self.fcList:
                print("KOMEKCI layi yoxdur ve ya adi duzgun yazilmayib!")
            if "HATLAR" not in self.fcList:
                print("HATLAR layi yoxdur ve ya adi duzgun yazilmayib!")


            elif "TORPAQ_TUM" or  "TIKILI_TUM" or "SEKTOR" or "QUARTER" or "Noqteler" or "KOMEKCI" or "HATLAR" in self.fcList:
                print("it is okey")

        except:
            print("Bazanin yolu dogru gosterilmeyib!")

    def create_topology(self):
        print("Topologiya yaradilir...")
        
        try:
            ################# Topologiya yaradilir ###################
            arcpy.CreateTopology_management(self.database,"Topology")
            self.fcList = arcpy.ListFeatureClasses()
            for self.fcname in self.fcList:
                if self.fcname == "KOMEKCI" or "TORPAQ_TUM" or "TIKILI_TUM" or "SEKTOR" or "QUARTER":
                    arcpy.AddFeatureClassToTopology_management("Topology",self.fcname)
                    
            arcpy.AddRuleToTopology_management("Topology","Must Not Overlap With (Area-Area)",self.database+'\KOMEKCI',"",self.database+'\TIKILI_TUM',"")
            arcpy.AddRuleToTopology_management("Topology","Must Not Overlap (Area)",self.database+'\TORPAQ_TUM',"","")
            arcpy.AddRuleToTopology_management("Topology","Must Not Overlap (Area)",self.database+'\TIKILI_TUM',"","")
            arcpy.AddRuleToTopology_management("Topology","Must Not Overlap (Area)",self.database+'\SEKTOR',"","")
            arcpy.AddRuleToTopology_management("Topology","Must Not Overlap (Area)",self.database+'\QUARTER',"","")
            arcpy.AddRuleToTopology_management("Topology","Must Not Have Gaps (Area)",self.database+'\SEKTOR',"","")
            arcpy.AddRuleToTopology_management("Topology","Must Not Have Gaps (Area)",self.database+'\QUARTER',"","")
            arcpy.AddRuleToTopology_management("Topology","Must Not Have Gaps (Area)",self.database+'\TORPAQ_TUM',"","")
            arcpy.AddRuleToTopology_management("Topology","Must Be Covered By (Area-Area)",self.database+'\TIKILI_TUM',"",self.database+'\TORPAQ_TUM',"")
            arcpy.AddRuleToTopology_management("Topology","Must Be Covered By (Area-Area)",self.database+'\KOMEKCI',"",self.database+'\TORPAQ_TUM',"")
            arcpy.AddRuleToTopology_management("Topology","Must Be Covered By (Area-Area)",self.database+'\KOMEKCI',"",self.database+'\SEKTOR',"")
            arcpy.AddRuleToTopology_management("Topology","Must Be Covered By (Area-Area)",self.database+'\TIKILI_TUM',"",self.database+'\SEKTOR',"")
            arcpy.ValidateTopology_management("Topology")

            
            print("**************************************************************************************************")
            print("Topologiya quruldu...")
            print("**************************************************************************************************")

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Topologiyanin yaradilmasi prosesinde xeta bas verdi!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        try:
            print("Askarlanmis topoloji xetalar export edilir...")
            ################# Topoloji xetalar export edilir ###################
            arcpy.ExportTopologyErrors_management("Topology",self.output,"Topology")
            print("**************************************************************************************************")
            print(" Askarlanmis xetalar ugurla export edildi...")
            print("**************************************************************************************************")

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Xetalarin export edilmesi prosesinde xeta bas verdi!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


    def border_parcel_check(self):
        print("Erase emeliyyatlari aparilir...")
        
        try:
            ############### Quarter ve Sektorla torpaq parseli arasinda erase emeliyyatlari aparilir ################
            arcpy.Erase_analysis("SEKTOR","TORPAQ_TUM",self.output+"\Sektorla_Torpaq_Arasinda_Bosluq")
            arcpy.Erase_analysis("QUARTER","TORPAQ_TUM",self.output+"\Quarterle_Torpaq_Arasinda_Bosluq")
            arcpy.Erase_analysis("TORPAQ_TUM","SEKTOR",self.output+"\Torpaq_Sektordan_Kenarda")
            print("************************************************************************************************")
            print("Erase emeliyyatlari ugurla basa catdi! Neticeler xetalar ucun secilmis qovluga gonderildi.")
            print("************************************************************************************************")
        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Erase prosesinde xeta bas verdi! Databazaya baxin ve ya check_feature() -metodunu ise salin. Laylardan her hansisa standart deyil!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        print("Quarterin torpagi kesmesi yoxlanilir...")
        try:
            ########### Quarterin torpagi kesmesi yoxlanilir ####################
            arcpy.PolygonToLine_management("QUARTER",self.output+"\quarter_line")
            arcpy.SplitLine_management(self.output+"\quarter_line",self.output+"\split_line")
            arcpy.MakeFeatureLayer_management(self.output+"\split_line","make")
            arcpy.SelectLayerByLocation_management("make","SHARE_A_LINE_SEGMENT_WITH","TORPAQ_TUM","","NEW_SELECTION","INVERT")
            
            
            count = str(arcpy.GetCount_management("make"))
            if count!="0":
                arcpy.CopyFeatures_management("make",self.output+"\Quarter_torpagi_kesir")
                print("************************************************************************************************")
                print("Quarter torpagi kesir. Netice Xetalar ucun secilmis qovluguna gonderildi...")
                print("************************************************************************************************")
            else:
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                print("Hec bir xeta askarlanmadigi ucun netice xetalar ucun secilmis qovluga gonderilmedi...")
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

            print("################################################################################################")
            print("Quarterin torpagi kesmesinin yoxlanilma prosesi ugurla basa catdi!")
            print("################################################################################################")

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Quarterin torpagi kesmesinin yoxlanilmasi prosesinde xeta bas verdi! Databazaya baxin ve ya check_feature() -metodunu ise salin. Laylardan her hansisa standart deyil!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        print("Sektorun torpagi kesmesi yoxlanilir...")

        try:
            ####### Sektorun torpagi kesmesi yoxlanilir ############
            arcpy.PolygonToLine_management("SEKTOR",self.output+"\sektor_line")
            arcpy.SplitLine_management(self.output+"\sektor_line",self.output+"\split_line_2")
            arcpy.MakeFeatureLayer_management(self.output+"\split_line_2","make")
            arcpy.SelectLayerByLocation_management("make","SHARE_A_LINE_SEGMENT_WITH","TORPAQ_TUM","","NEW_SELECTION","INVERT")
            
            
            count = str(arcpy.GetCount_management("make"))
            if count!="0":
                arcpy.CopyFeatures_management("make",self.output+"\Sektor_torpagi_kesir")
                print("************************************************************************************************")
                print("Sektor torpagi kesir. Netice Xetalar ucun secilmis qovluguna gonderildi...")
                print("************************************************************************************************")
            else:
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                print("Hec bir xeta askarlanmadigi ucun netice xetalar ucun secilmis qovluga gonderilmedi...")
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

            print("################################################################################################")
            print("Sektorun torpagi kesmesinin yoxlanilma prosesi ugurla basa catdi!")
            print("################################################################################################")

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Sektorun torpagi kesmesinin yoxlanilmasi prosesinde xeta bas verdi! Databazaya baxin ve ya check_feature() -metodunu ise salin. Laylardan her hansisa standart deyil!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    def quarter_building_check(self):
        print("Quarterin komekcini kesmesi yoxlanilir...")
        try:
            ############# Quarterin komekci layini kesmesi yoxlanilir ############
            arcpy.PolygonToLine_management("QUARTER",self.output+"\quarter_line_2")
            arcpy.Intersect_analysis(["KOMEKCI",self.output+"\quarter_line_2"],self.output+"\quarter_komekci_intersect")
            arcpy.MakeFeatureLayer_management(self.output+"\quarter_komekci_intersect","make_2")
            
            arcpy.SelectLayerByLocation_management("make_2","SHARE_A_LINE_SEGMENT_WITH","KOMEKCI","","NEW_SELECTION","INVERT")

            count_komekci = str(arcpy.GetCount_management("make_2"))

            if count_komekci!="0":
                arcpy.CopyFeatures_management("make_2",self.output+"\Quarter_komekcini_kesir")
                print("************************************************************************************************")
                print("Quarter komekcini kesir kesir. Netice Xetalar ucun secilmis qovluguna gonderildi...")
                print("************************************************************************************************")

            else:
                print("################################################################################################")
                print("Quarter komekcini kesmir! Xetalar ucun qeyd edilmis bazaya hec bir lay gonderilmedi!")
                print("################################################################################################")

            print("################################################################################################")
            print("Quarterin komekcini kesmesinin, yoxlanilma prosesi ugurla basa catdi!")
            print("################################################################################################")
         

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Quarterin komekcini kesme prosesinde xeta bas verdi!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        print("Quarterin tikilini kesmesi yoxlanilir...")

        try:
            ########## Quarterin tikili layini kesmesi yoxlanilir #############
            arcpy.PolygonToLine_management("QUARTER",self.output+"\quarter_line_3")
            arcpy.Intersect_analysis(["TIKILI_TUM",self.output+"\quarter_line_3"],self.output+"\quarter_tikili_intersect")
            arcpy.MakeFeatureLayer_management(self.output+"\quarter_tikili_intersect","make_3")
            arcpy.SelectLayerByLocation_management("make_3","SHARE_A_LINE_SEGMENT_WITH","TIKILI_TUM","","NEW_SELECTION","INVERT")

            count_tikili = str(arcpy.GetCount_management("make_3"))
            if count_tikili!="0":
                arcpy.CopyFeatures_management("make_3",self.output+"\Quarter_tikilini_kesir")
                print("************************************************************************************************")
                print("Quarter tikilini kesir kesir. Netice Xetalar ucun secilmis qovluguna gonderildi...")
                print("************************************************************************************************")

            else:
                print("################################################################################################")
                print("Quarter tikilini kesmir! Xetalar ucun qeyd edilmis bazaya hec bir lay gonderilmedi!")
                print("################################################################################################")

            print("################################################################################################")
            print("Quarterin tikili kesmesinin, yoxlanilma prosesi ugurla basa catdi!")
            print("################################################################################################")
         



        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Quarterin komekcini kesme prosesinde xeta bas verdi!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        

    def delete_extra_layer(self):
        print("Prosesler zamani yaranmis elave laylar silinir...")
        try:
            ######### Prosesleri zamani yaradilmis elave laylar bu ,etod vasitesile silinir ##############
            env.workspace = self.output
            self.fclassList = arcpy.ListFeatureClasses("*")
            for self.fclass in self.fclassList:
                if self.fclass == "quarter_line_3":
                    arcpy.Delete_management(self.fclass)
                if self.fclass == "quarter_line_2":
                    arcpy.Delete_management(self.fclass)

                if self.fclass == "quarter_line":
                    arcpy.Delete_management(self.fclass)

                if self.fclass == "quarter_komekci_intersect":
                    arcpy.Delete_management(self.fclass)

                if self.fclass == "quarter_tikili_intersect":
                    arcpy.Delete_management(self.fclass)

                if self.fclass == "split_line":
                    arcpy.Delete_management(self.fclass)

                if self.fclass == "split_line_2":
                    arcpy.Delete_management(self.fclass)
                if self.fclass == "sektor_line":
                    arcpy.Delete_management(self.fclass)

                if self.fclass == "point_building":
                    arcpy.Delete_management(self.fclass)


            print("************************************************************************************************")
            print("Prosesler zamani yaranmis elave laylar databazadan ugurla silindi!...")
            print("************************************************************************************************")

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Elave laylarin silinmesi prosesinde xeta bas verdi!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        
    def check_field_value_full(self):
        ############### Torpaq ve tikili layinda olan atribut melumatlarinin tam doldurulmasi yoxlanilir ##############
        print("Atribut melumatlarinin tam doldurulmasi yoxlanilir...")
        try:

            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","EMLAK_NOVU is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Emlak_novu_sutunu_bosdur","INSIDE")
                print("Emlak novu sutununda bos olan melumat var!")

            else:
                print("Emlak novu sutununda bos olan melumat yoxdur!")

        except:
            print("Emlak novu sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi!")


        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","T_KATEGORI is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Torpagin_kateqoriyasi_bosdur","INSIDE")
                print("Kateqoriya sutununda bos olan melumat var!")

            else:
                print("Kateqoriya sutununda bos olan melumat yoxdur!")

        except:
            print("Kateqoriya sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi!")


        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","ALT_KATEGORI is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Alt_kateqoriya_bosdur","INSIDE")
                print("Alt kateqoriya sutununda bos olan melumat var!")

            else:
                print("Alt kateqoriya sutununda bos olan melumat yoxdur!")

        except:
            print("Alt kateqoriya sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","ALT_IST_NOVU is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Alt_ist_novu_sutunu_bosdur","INSIDE")
                print("ALT_IST_NOVU sutununda bos olan melumat var!")

            else:
                print("ALT_IST_NOVU sutununda bos olan melumat yoxdur!")

        except:
            print("ALT_IST_NOVU sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","MULKFORM is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Mulkiyyet_sutunu_bosdur","INSIDE")
                print("MULKFORM sutununda bos olan melumat var!")

            else:
                print("MULKFORM sutununda bos olan melumat yoxdur!")

        except:
            print("MULKFORM sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","ISTIFADE is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Istifade_sutunu_bosdur","INSIDE")
                print("ISTIFADE sutununda bos olan melumat var!")

            else:
                print("ISTIFADE sutununda bos olan melumat yoxdur!")

        except:
            print("ISTIFADE sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","LEQAL_MI is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Leqalliq_sutunu_bosdur","INSIDE")
                print("LEQAL_MI sutununda bos olan melumat var!")

            else:
                print("LEQAL_MI sutununda bos olan melumat yoxdur!")

        except:
            print("LEQAL_MI sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("SEKTOR","sektor")
            arcpy.SelectLayerByAttribute_management("sektor","NEW_SELECTION","SECTOR_NAME is null")
            arcpy.MakeFeatureLayer_management("sektor","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("process",self.output+"\Sector_sutunu_bosdur","INSIDE")
                print("SECTOR_NAME sutununda bos olan melumat var!")

            else:
                print("SECTOR_NAME sutununda bos olan melumat yoxdur!")

        except:
            print("SECTOR_NAME sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi! Sutun adi standarta uygun deyil!")

        
        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","TIKILI_NOVU is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Tikili_novu_sutunu_bosdur")

                print("Tikili novu sutunu bosdur !")

            else:
                print("Tikili novu sutununda bos olan melumat yoxdur !")

        except:
            print("Tikili novunun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","MATERYAL is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Materiyal_sutunu_bosdur","INSIDE")

                print("Materiyal sutunu bosdur !")

            else:
                print("Materiyal sutununda bos olan melumat yoxdur !")

        except:
            print("Materiyal sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","YARIMCIQ is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Yarimciq_sutunu_bosdur","INSIDE")

                print("Yarimciq sutunu bosdur !")

            else:
                print("Yarimciq sutununda bos olan melumat yoxdur !")

        except:
            print("Yarimciq sutununun yoxlanilmasinda xeta bas verdi !")



        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","MULKFORM is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Mulkiyyet_sutunu_bosdur_tikilide","INSIDE")

                print("Mulkiyyet sutunu bosdur !")

            else:
                print("Mulkiyyet sutununda bos olan melumat yoxdur !")

        except:
            print("Mulkiyyet sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","ISTIFADE is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Istifade_sutunu_bosdur_tikilide","INSIDE")

                print("Istifade sutunu bosdur !")

            else:
                print("Istifade sutununda bos olan melumat yoxdur !")


        except:
            print("Istifade sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","LEQAL_MI is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Leqal_sutunu_bosdur_tikilide","INSIDE")

                print("Leqal sutunu bosdur !")

            else:
                print("Leqal sutununda bos olan melumat yoxdur !")

        except:
            print("Leqal sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","QAZ is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Qaz_sutunu_bosdur","INSIDE")

                print("Qaz sutunu bosdur !")

            else:
                print("Qaz sutununda bos olan melumat yoxdur !")

        except:
            print("Qaz sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","SU is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Su_sutunu_bosdur","INSIDE")

                print("Su sutunu bosdur !")

            else:
                print("Su sutununda bos olan melumat yoxdur !")


        except:
            print("Su sutununun yoxlanilmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","ISIK is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Isik_sutunu_bosdur","INSIDE")

                print("Isik sutunu bosdur !")

            else:
                print("Isik sutununda bos olan melumat yoxdur !")

        except:
            print("Isik sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","ISTILIK_SISTEMI is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Istilik_sistemi_sutunu_bosdur","INSIDE")

                print("Istilik sistemi sutunu bosdur !")

            else:
                print("Istilik sistemi sutununda bos olan melumat yoxdur !")


        except:
            print("Istilik sistemi sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","ISTI_SU is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Isti_su_sutunu_bosdur","INSIDE")

                print("Isti su sistemi sutunu bosdur !")

            else:
                print("Isti su sistemi sutununda bos olan melumat yoxdur !")

        except:
            print("Isti su sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","TELEFON is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Telefon_sutunu_bosdur","INSIDE")

                print("Telefon  sutunu bosdur !")

            else:
                print("Telefon  sutununda bos olan melumat yoxdur !")

        except:
            print("Telefon sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","KANALIZASIYA is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Kanalizasiya_sutunu_bosdur","INSIDE")

                print("Kanalizasiya sutunu bosdur !")

            else:
                print("Kanalizasiya sutununda bos olan melumat yoxdur !")


        except:
            print("Kanalizasiya sutununun yoxlanilmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","UNVAN is null")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            count_torpaq = str(arcpy.GetCount_management("tikili2"))

            if count_torpaq!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Unvan_sutunu_bosdur","INSIDE")

                print("Unvan sutunu bosdur !")

            else:
                print("Unvan sutununda bos olan melumat yoxdur !")


        except:
            print("Unvan sutununun yoxlanilmasinda xeta bas verdi !")

            



    def check_atribute(self):

######### Torpaq ve tikili layinin atribut melumatlari ve aralarinda qarsiliqli uygunluq yoxlanilir ###########################


        print("Atribut melumatlari yoxlanilir...")
        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_emlak","(EMLAK_NOVU = 0 AND ALT_IST_NOVU NOT IN(1,3,5,7,10,11,12,13,20,21,22,25,27,31,32,42,51,53,61,62,63,66,67,77,80,82,91,94,95,97,98,99,100,101,102,103,105,107,109,110,113,117,118,123,124,126,130,135,137,138,139,146,149,151,152,153,159,160,161,115)) OR (EMLAK_NOVU =1 AND ALT_IST_NOVU NOT IN (0,2,6,8,15,26,35,39,44,119,128,129,131,132)) OR (EMLAK_NOVU =3 AND ALT_IST_NOVU NOT IN(17,18,81,121,140,145)) OR  (EMLAK_NOVU = 9 AND ALT_IST_NOVU NOT IN(38)) OR (EMLAK_NOVU = 4 AND ALT_IST_NOVU NOT IN( 19 )) OR (EMLAK_NOVU = 11 AND ALT_IST_NOVU NOT IN(16,30,36,41,50,55,65,68,89,90,96,111,122,136,141,143,144,158,162)) OR (EMLAK_NOVU = 13 AND ALT_IST_NOVU NOT IN(23,64,106,154,155,156,157)) OR (EMLAK_NOVU = 2 AND ALT_IST_NOVU NOT IN(56,74,75,76,78,79,87,104,112)) OR (EMLAK_NOVU =12 AND ALT_IST_NOVU NOT IN(9,86,114,125)) OR (EMLAK_NOVU = 6 AND ALT_IST_NOVU NOT IN(14,29,33,34,43,54,84,85,120,127)) OR (EMLAK_NOVU =14 AND ALT_IST_NOVU NOT IN(37,52,69))")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_emlak"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_emlak",self.output+"\Emlak_novu_uqodiyasi_arasinda_uygunsuzluq","INSIDE")
                print("Emlak novu ile uqodiya arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Emlak novu ile uqodiya arasinda uygunsuzluq yoxdur!")
        except:
            print("Emlak novu ile uqodiyanin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_kateqoriya","(T_KATEGORI = 0 AND ALT_KATEGORI NOT IN(0,1,2,3,4)) OR (T_KATEGORI = 1 AND ALT_KATEGORI NOT IN(5,6,7)) OR (T_KATEGORI =2 AND ALT_KATEGORI NOT IN(8,9,10,11,12)) OR (T_KATEGORI =3 AND ALT_KATEGORI NOT IN(18,19,20,21,22)) OR (T_KATEGORI =4 AND ALT_KATEGORI NOT IN(13)) OR (T_KATEGORI =6 AND ALT_KATEGORI NOT IN(23)) OR ( T_KATEGORI = 5 AND ALT_KATEGORI NOT IN(14,15,16,17) )")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_kateqoriya"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_kateqoriya",self.output+"\Kateqoriyasi_alt_kateqoriyasi_arasinda_uygunsuzluq","INSIDE")
                print("Kateqoriya ile alt kateqoriya arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Kateqoriya ile alt kateqoriya arasinda uygunsuzluq yoxdur!")
        except:
            print("Kateqoriya ile alt kateqoriya yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_altkateqoriya","(ALT_KATEGORI = 5 AND ALT_IST_NOVU NOT IN( 0 ,12,17,18,31,32,38,42,51,81,121,135,140,145)) OR (ALT_KATEGORI = 6  AND ALT_IST_NOVU NOT IN(1,3,4,9,14,16,24,25,29,30,33,34,36,37,40,41,43,44,45,46,47,48,49,50,52,54,55,58,59,60,65,68,69,70,71,72,82,83,84,85,86,88,89,90,92,93,96,108,111,114,120,122,125,127,133,134,136,137,139,141,142,143,144,147,149,150,152,158,162)) OR (ALT_KATEGORI = 7  AND ALT_IST_NOVU NOT IN(2,5,6,7,8,10,11,13,15,19,20,21,22,23,26,27,28,35,39,53,56,57,61,62,63,64,66,67,73,74,75,76,77,78,79,80,87,91,94,95,97,98,99,100,101,102,103,104,105,106,107,109,110,112,113,116,117,118,119,123,124,126,128,129,130,131,132,138,146,151,153,154,155,156,157,159,160))")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_altkateqoriya"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_altkateqoriya",self.output+"\Alt_kateqoriya_uqodiya_arasinda_ferq","INSIDE")
                print("Alt kateqoriya ile alt istifade novu arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Alt kateqoriya ile alt istifade novu arasinda uygunsuzluq yoxdur!")
        except:
            print("Alt kateqoriya ile alt istifade novu yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_mulkreyestr","(mid ([REYESTR_NO],6,1) ='3' AND [MULKFORM] <>2) OR (mid ([REYESTR_NO],6,1) <> '3' AND [MULKFORM] =2) OR (mid ([REYESTR_NO],6,1) ='2' AND [MULKFORM] <>1) OR (mid ([REYESTR_NO],6,1) <>'2' AND [MULKFORM] =1) OR (mid ([REYESTR_NO],6,1) ='1' AND [MULKFORM] <>0) OR (mid ([REYESTR_NO],6,1) <> '1' AND [MULKFORM]=0)")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_mulkreyestr"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_mulkreyestr",self.output+"\Mulkiyyeti_ile_reyestr_nomresi_arasinda_uygunsuzluqlar","INSIDE")
                print("Mulkiyyet ile reyestr nomresi arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Mulkiyyet ile reyestr nomresi arasinda uygunsuzluq yoxdur!")
        except:
            print("Mulkiyyet ile reyestr nomresi yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","altkateqoriyamulkiyyet","[ALT_KATEGORI] = 7 AND [MULKFORM] = 2")
            count_torpaq_atribut = str(arcpy.GetCount_management("altkateqoriyamulkiyyet"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("altkateqoriyamulkiyyet",self.output+"\Alt_kateqoriyasi_umumi_istifade_mulkiyyeti_xususidir","INSIDE")
                print("Alt kateqoriya ile mulkiyyet arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Alt kateqoriya ile mulkiyyet arasinda uygunsuzluq yoxdur!")
        except:
            print("Alt kateqoriya ile mulkiyyet yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","kateqoriyamulkiyyet","T_KATEGORI IN(4,5) AND MULKFORM =2")
            count_torpaq_atribut = str(arcpy.GetCount_management("kateqoriyamulkiyyet"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("kateqoriyamulkiyyet",self.output+"\Kateqoriyasi_mese_ve_su_fondu_mulkiyyet_xususi","INSIDE")
                print("Kateqoriya ile mulkiyyet arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Kateqoriya ile mulkiyyet arasinda uygunsuzluq yoxdur!")
        except:
            print("Kateqoriya ile mulkiyyet yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senedsekilsenednov","SENEDSEKIL IS NOT NULL AND SENEDNOVU IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("senedsekilsenednov"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senedsekilsenednov",self.output+"\Senedsekili_var_senednovu_yoxdur","INSIDE")
                print("Sened sekili var, lakin sened novu yoxdur! Xetalara gonderildi...")

            else:
                print("Sened sekili ile sened novu arasinda uygunsuzluq yoxdur!")
        except:
            print("Sened sekili ile sened novunun yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","reyestrsened","REYESTR_NO IS NOT NULL AND SENEDNOVU IS NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("reyestrsened"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("reyestrsened",self.output+"\Reyestr_nomresi_var_senednovu_sahesi_yoxdur","INSIDE")
                print("Reyestr nomresi var lakin sened novu ve sahesi yoxdur! Xetalara gonderildi...")

            else:
                print("Reyestr ile sened novu ve sahe arasinda uygunsuzluq askarlanmadi!")
        except:
            print("Reyestr ile sened novu sahenin yoxlanmas prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senednovuleqalliq","SENEDNOVU IN(7,10,11,12,13) AND LEQAL_MI = 0")
            count_torpaq_atribut = str(arcpy.GetCount_management("senednovuleqalliq"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senednovuleqalliq",self.output+"\Senednovu_var_legalligi_xeyr","INSIDE")
                print("Sened novu var lakin leqalligi xeyr qeyd edilib! Xetalara gonderildi...")

            else:
                print("Sened novu ile leqalliq arasinda xeta askarlanmadi!")
        except:
            print("Sened novu ile leqalligin yoxlanilmasi prosesinde xeta bas verdi!")


        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senednovuleqalliq","SENEDNOVU IS NULL AND LEQAL_MI = 1 AND MULKFORM=0")
            count_torpaq_atribut = str(arcpy.GetCount_management("senednovuleqalliq"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senednovuleqalliq",self.output+"\Senednovu_var_legalligi_xeyr","INSIDE")
                print("Sened novu var lakin leqalligi xeyr qeyd edilib! Xetalara gonderildi...")

            else:
                print("Sened novu ile leqalliq arasinda xeta askarlanmadi!")
        except:
            print("Sened novu ile leqalligin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senednovsekil","SENEDNOVU IS NOT NULL AND SENEDSEKIL IS NOT NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("senednovsekil"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senednovsekil",self.output+"\Senednovu_senedsekili_var_sahesi_yoxdur","INSIDE")
                print("Sened novu, senedsekili var sahesi yoxdur! Xetalara gonderildi...")

            else:
                print("Sened novu ile sahesi arasinda uygunsuzluq askarlanmadi!")
        except:
            print("Sened novu senedsekili ve sahenin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","reyestrnomresistandart","Len( REYESTR_NO) <>12 AND Len( REYESTR_NO) <>18")
            count_torpaq_atribut = str(arcpy.GetCount_management("reyestrnomresistandart"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("reyestrnomresistandart",self.output+"\Reyestr_nomreleri_standart_deyil","INSIDE")
                print("Reyestr nomresi standart deyil! Xetalara gonderildi...")

            else:
                print("Qeyri standart reyestr nomresi askarlanmadi !")
        except:
            print("Reyestr nomresinin standartliginin yoxlanilmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senednovsenedsekilreyestr","SENEDNOVU IN(10,12) AND SENEDSEKIL IS NOT NULL AND REYESTR_NO IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("senednovsenedsekilreyestr"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senednovsenedsekilreyestr",self.output+"\senednovu_senedsekili_var_reyestri_yoxdur","INSIDE")
                print("Sened novu var sened sekili var reyestr yoxdu! Xetalara gonderildi...")

            else:
                print("Sened novu sened sekili olanlarin reyestr var !")
        except:
            print("Sene novu sened sekili olanlarin reyestrinin yoxlanmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","reyestrleqalliq","REYESTR_NO IS NOT NULL AND LEQAL_MI = 0")
            count_torpaq_atribut = str(arcpy.GetCount_management("reyestrleqalliq"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("reyestrleqalliq",self.output+"\Reyestr_nomresi_var_legalligi_xeyr","INSIDE")
                print("Reyestr nomresi var leqalligi xeyir qeyd edilib! Xetalara gonderildi...")

            else:
                print("Reyestr olub leqalligi xeyr qeyd edilen obyekt yoxdur !")
        except:
            print("Reyestr ile leqalligin yoxlanilmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","dovmulkiyyet","MULKFORM = 0 AND LEQAL_MI = 0 AND ISTIFADE = 0")
            count_torpaq_atribut = str(arcpy.GetCount_management("dovmulkiyyet"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("dovmulkiyyet",self.output+"\Dovlet_mulkiyyeti_olub_legalligi_xeyr_olanlar","INSIDE")
                print("Dovlet mulkiyyetidir leqalligi xeyr qeyd edilib ! Xetalara gonderildi...")

            else:
                print("Dovlet mulkiyyeti olub leqalligi xeyr qeyd edilen parseller yoxdur !")
        except:
            print("Dovlet mulkiyyeti ile leqalligin yoxlanilmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","belediyyeistifade","MULKFORM = 1 AND ISTIFADE = 2 AND LEQAL_MI = 1 AND SENEDNOVU IS NULL AND SENEDSEKIL IS NULL AND REYESTR_NO IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("belediyyeistifade"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("belediyyeistifade",self.output+"\Mukiyyeti_belediyye_istifadeci_olub_senednovu_senedsekili_reyestri_olmayan_lakin_leqal_olan","INSIDE")
                print("Mulkiyyeti belediyyedir sened novu sened sekili ve reyestr yoxdur lakin leqalligi beli qeyd edilib ! Xetalara gonderildi...")

            else:
                print("Mulkiyyeti belediyyedir sened novu sened sekili ve reyestr yoxdur lakin leqalligi beli qeyd edilen obyektler movcud deyil !")
        except:
            print("Belediyye mulkiyyeti olub senedi olmayib leqalligi beli olan obyektlerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_ferdi")
            arcpy.SelectLayerByAttribute_management("tikili_ferdi","NEW_SELECTION","TIKILI_NOVU = 16")
            arcpy.FeatureToPoint_management("tikili_ferdi",self.output+"\point_building")
            
            arcpy.MakeFeatureLayer_management(self.output+"\point_building","tikili_noqte")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_ferdi")
            arcpy.SelectLayerByLocation_management("torpaq_ferdi","INTERSECT","tikili_noqte","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("torpaq_ferdi","torpaq_ferdi2")
           
            arcpy.SelectLayerByAttribute_management("torpaq_ferdi2","NEW_SELECTION","EMLAK_NOVU=9")
            arcpy.SelectLayerByAttribute_management("torpaq_ferdi2","SWITCH_SELECTION","")
            arcpy.MakeFeatureLayer_management("torpaq_ferdi2","torpaq_ferdi3")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_ferdi3"))
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_ferdi3",self.output+"\Tikilisi_ferdi_yasayis_torpaq_ferqli","INSIDE")


                print("Tikilisi ferdi yasayis olub torpaginin emlak novu ferdi yasayis olmayanlar xeta kimi gonderildi !")
           
        except:
            print("Tikilisi ferdi yasayis torpagi ferqli olan parselin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_xususi")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_xususi")
            arcpy.SelectLayerByAttribute_management("torpaq_xususi","NEW_SELECTION","MULKFORM=2")
            arcpy.MakeFeatureLayer_management("torpaq_xususi","torpaq_xususi2")
            arcpy.SelectLayerByLocation_management("tikili_xususi","WITHIN","torpaq_xususi2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili_xususi","tikili_xususi2")
            arcpy.SelectLayerByAttribute_management("tikili_xususi2","NEW_SELECTION","MULKFORM<>2")
            arcpy.MakeFeatureLayer_management("tikili_xususi2","tikili_xususi3")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_xususi3"))
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_xususi3",self.output+"\Torpagi_xususi_tikilisi_ferqli","INSIDE")

                print("Torpaq xususi olub tikilisi ferqli olan obyektler xetalara gonderildi !")



            
           
        except:
            print("Torpaq xususi olub tikilisi ferqli olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_coxmertebeli")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_coxmertebeli")
            arcpy.SelectLayerByAttribute_management("torpaq_coxmertebeli","NEW_SELECTION","EMLAK_NOVU=4")
            arcpy.MakeFeatureLayer_management("torpaq_coxmertebeli","torpaq_coxmertebeli2")
            arcpy.SelectLayerByLocation_management("tikili_coxmertebeli","WITHIN","torpaq_coxmertebeli2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili_coxmertebeli","tikili_coxmertebeli2")
            arcpy.SelectLayerByAttribute_management("tikili_coxmertebeli2","NEW_SELECTION","TIKILI_NOVU=16")
            arcpy.MakeFeatureLayer_management("tikili_coxmertebeli2","tikili_coxmertebeli3")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_coxmertebeli3"))
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_coxmertebeli3",self.output+"\Torpagi_coxmertebeli_tikilisi_ferdi_yasayis","INSIDE")

                print("Torpaq coxmertebeli tikilisi ferdi yasayis olan obyektler xetalara gonderildi !")



            
           
        except:
            print("Torpaq coxmertebeli tikilisi ferdi yasayis olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_senednovyox","SENEDSEKIL IS NOT NULL AND SENEDNOVU IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_senednovyox"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_senednovyox",self.output+"\Senedsekili_var_Sened_Novu_Yoxdur_tikili","INSIDE")

                print("Sened sekili olub sened novu olmayan obyektler askarlanaraq xetalara gonderildi !")

            else:
                print("Sened sekili olub sened novu olmayan obyektler yoxdur")

                        
           
        except:
            print("Sened sekili olub sened novu olmayan obyektlerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_senednovusahesiyox","REYESTR_NO IS NOT NULL AND SENEDNOVU IS NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_senednovusahesiyox"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_senednovusahesiyox",self.output+"\Reyestri_var_senednovu_sahesi_yoxdur_tikili","INSIDE")

                print("Reyestri olub sened novu ve sahesi olmayan tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Reyestri olub sened novu ve sahesi olmayan tikililer yoxdur")

                        
           
        except:
            print("Reyestri olub sened novu ve sahesi olmayan tikililerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_sahesiyox","REYESTR_NO IS NOT NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_sahesiyox"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_sahesiyox",self.output+"\Reyestri_var_sahesi_yoxdur_tikili","INSIDE")

                print("Reyestri olub sahesi olmayan tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Reyestri olub sahesi olmayan tikililer yoxdur")

                        
           
        except:
            print("Reyestri olub sahesi olmayan tikililerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_mertebe","YARIMCIQ=0 AND MERTEBE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_mertebe"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_mertebe",self.output+"\Tikili_yarimciq_deyil_mertebesi_qeyd_edilmeyib","INSIDE")

                print("Yarimciq olmayib lakin mertebesi qeyd edilmeyen tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Yarimciq olmayib mertebesi qeyd edilmeyen tikili askarlanmadi")

                        
           
        except:
            print("Yarimciq olmayib mertebesi qeyd edilmeyen tikililerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_torpaqsahesi")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_torpaqsahesi")
            arcpy.SelectLayerByLocation_management("torpaq_torpaqsahesi","CONTAINS","tikili_torpaqsahesi","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("torpaq_torpaqsahesi","torpaq_torpaqsahesi2")
            arcpy.SelectLayerByAttribute_management("torpaq_torpaqsahesi2","NEW_SELECTION","EMLAK_NOVU=0")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_torpaqsahesi2"))
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_torpaqsahesi2",self.output+"\Tikilisi_var_torpaq_torpaq_sahesidir","INSIDE")

                print("Tikilisi olub torpagi torpaq sahesi olan obyektler xetalara gonderildi !")



            
           
        except:
            print("Tikilisi olub torpagi torpaq sahesi olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_saheeyoxox","SENEDNOVU IS NOT NULL AND SENEDSEKIL IS NOT NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_saheeyoxox"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_saheeyoxox",self.output+"\Senednovu_senedsekili_var_sahesi_yoxdur_tikili","INSIDE")

                print("Senednovu senedsekili olub sahesi olmayan tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Senednovu senedsekili olub sahesi qeyd edilmeyen tikili askarlanmadi")

                        
           
        except:
            print("Senednovu senedsekili olub sahesi qeyd edilmeyen tikililerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_reyestrryoxx","SENEDNOVU =12 AND REYESTR_NO IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_reyestrryoxx"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_reyestrryoxx",self.output+"\Senednovu_var_reyestri_yoxdur_tikili","INSIDE")

                print("Senednovu olub reyestr olmayan tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Senednovu olub reyestri qeyd edilmeyen tikili askarlanmadi")

                        
           
        except:
            print("Senednovu olub reyestri qeyd edilmeyen tikililerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_ferditikiliii")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_ferditikiliii")
            arcpy.SelectLayerByAttribute_management("torpaq_ferditikiliii","NEW_SELECTION","EMLAK_NOVU=9")
            arcpy.MakeFeatureLayer_management("torpaq_ferditikiliii","torpaq_ferditikiliii2")
            arcpy.SelectLayerByLocation_management("tikili_ferditikiliii","WITHIN","torpaq_ferditikiliii2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili_ferditikiliii","tikili_ferditikiliii2")
            arcpy.SelectLayerByAttribute_management("tikili_ferditikiliii2","NEW_SELECTION","TIKILI_NOVU<>16")
            arcpy.MakeFeatureLayer_management("tikili_ferditikiliii2","tikili_ferditikiliii3")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_ferditikiliii3"))
          
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_ferditikiliii3",self.output+"\Torpagi_ferdi_yasayis_tikilisi_ferqli","INSIDE")

                print("Torpagi ferdi yasayis tikilisi ferqli olan obyektler xetalara gonderildi !")



            
           
        except:
            print("Torpagi ferdi yasayis tikilisi ferqli olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_qeyriyas")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_qeyriyas")
            arcpy.SelectLayerByAttribute_management("torpaq_qeyriyas","NEW_SELECTION","EMLAK_NOVU=5 AND ALT_IST_NOVU NOT IN (4,24,28,40,45,46,47,48,49,57,58,59,60,70,71,72,73,83,88,92,93,108,116,133,134,142,147,150)")
            arcpy.MakeFeatureLayer_management("torpaq_qeyriyas","torpaq_qeyriyas2")
            arcpy.SelectLayerByLocation_management("tikili_qeyriyas","WITHIN","torpaq_qeyriyas2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili_qeyriyas","tikili_qeyriyas2")
            arcpy.SelectLayerByAttribute_management("tikili_qeyriyas2","NEW_SELECTION","TIKILI_NOVU=16")
            arcpy.MakeFeatureLayer_management("tikili_qeyriyas2","tikili_qeyriyas3")
            arcpy.SelectLayerByLocation_management("torpaq_qeyriyas2","CONTAINS","tikili_qeyriyas3","","","NOT_INVERT")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_qeyriyas2"))
          
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_qeyriyas2",self.output+"\Emlak_novu_qeyri_yasayisdir_uzerinde_ferdiyasayis_tikilisi_var_uqodiyayabax","INSIDE")

                print("Emlak novu qeyri yasayis olub uzerinde ferdi yasayis tikilisi olub uqodiyasi yanlis olan obyektler xetalara gonderildi !")

            else:
                print("Emlak novu qeyriyasayis olan obyektlerin uzerinde ferdi yoxdur. Uygunluq pozulmayib")



            
           
        except:
            print("Emlak novu qeyri yasayis olub uzerinde ferdi yasayis tikilisi olub uqodiyasi yanlis olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:
           
            
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_uzerindetikiliyox")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_uzerindetikiliyox")
            arcpy.MakeFeatureLayer_management("KOMEKCI","komekci_uzerindetikiliyox")
            arcpy.SelectLayerByAttribute_management("torpaq_uzerindetikiliyox","NEW_SELECTION","EMLAK_NOVU=5 AND ALT_IST_NOVU NOT IN (4,24,28,40,45,46,47,48,49,57,58,59,60,70,71,72,73,83,88,92,93,108,116,133,134,142,147,150)")
            arcpy.MakeFeatureLayer_management("torpaq_uzerindetikiliyox","torpaq_uzerindetikiliyox2")
            arcpy.SelectLayerByLocation_management("torpaq_uzerindetikiliyox2","CONTAINS","tikili_uzerindetikiliyox","","","INVERT")
            arcpy.MakeFeatureLayer_management("torpaq_uzerindetikiliyox2","torpaq_uzerindetikiliyox3")
            arcpy.SelectLayerByLocation_management("torpaq_uzerindetikiliyox3","CONTAINS","komekci_uzerindetikiliyox","","","INVERT")
            arcpy.MakeFeatureLayer_management("torpaq_uzerindetikiliyox3","torpaq_uzerindetikiliyox4")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_uzerindetikiliyox4"))

               
          
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_uzerindetikiliyox4",self.output+"\Emlak_novu_qeyri_yasayisdir_uzerinde_tikili_yoxdur_uqodiyayabax","INSIDE")

                print("Emlak novu qeyri yasayis olub uzerinde tikilisi yoxdur uqodiyasi yanlis olan obyektler xetalara gonderildi !")

            else:
                print("Emlak novu qeyri yasayis olub uzerinde tikilisi var uqodiyada problem yoxdur !")



            
           
        except:
            print("Emlak novu qeyri yasayis olub uzerinde tikilisi yoxdur uqodiyasi yanlis olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:      
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_feerditikyox")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_feerditikyox")
            arcpy.SelectLayerByAttribute_management("torpaq_feerditikyox","NEW_SELECTION","EMLAK_NOVU=9")
            arcpy.MakeFeatureLayer_management("torpaq_feerditikyox","torpaq_feerditikyox2")
            arcpy.SelectLayerByLocation_management("torpaq_feerditikyox2","CONTAINS","tikili_feerditikyox","","","INVERT")
            arcpy.MakeFeatureLayer_management("torpaq_feerditikyox2","torpaq_feerditikyox3")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_feerditikyox3"))

               
          
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_feerditikyox3",self.output+"\Emlak_novu_ferdi_yasayis_uzerinde_tikili_yox","INSIDE")

                print("Emlak novu ferdi yasayis olub uzerinde tikilisi olmayan obyektler xetalara gonderildi !")

            else:
                print("Emlak novu ferdi yasayis olan torpaqlarin hamisinin uzerinde tikilisi var !")



            
           
        except:
            print("Emlak novu ferdi yasayis olub uzerinde tikilisi olmayan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:      
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_infstruktur")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_infstruktur")
            arcpy.SelectLayerByAttribute_management("torpaq_infstruktur","NEW_SELECTION","ALT_IST_NOVU IN(5,66,130,159,160,161)")
            arcpy.MakeFeatureLayer_management("torpaq_infstruktur","torpaq_infstruktur2")
            arcpy.SelectLayerByLocation_management("tikili_infstruktur","WITHIN","torpaq_infstruktur2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili_infstruktur","tikili_infstruktur2")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_infstruktur2"))

               
          
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_infstruktur2",self.output+"\Infrastruktur_uzerinde_tikili","INSIDE")

                print("Infrastruktur uzerinde tikili askarlandi, xetalara gonderildi !")

            else:
                print("Infrastruktur uzerinde tikili yerlesmir !")



            
           
        except:
            print("Infrastruktur uzerinde tikilinin yoxlanmasi prosesinde xeta bas verdi !")


        try:      
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_istmuddeti")
            arcpy.SelectLayerByAttribute_management("torpaq_istmuddeti","NEW_SELECTION","ISTIFADE IN(1,2) AND LEQAL_MI = 1 AND ISTIFADE_MUDDETI IS NULL")
            arcpy.MakeFeatureLayer_management("torpaq_istmuddeti","torpaq_istmuddeti2")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_istmuddeti2"))

               
          
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_istmuddeti2",self.output+"\Istifadesi_icareci_istifadecidir_istifade_muddeti_qeyd_edilmeyib","INSIDE")

                print("Istifadesi icareci ve istifadecidir istifade muddeti qeyd edilmeyib, xetalara gonderildi !")

            else:
                print("Istifadesi icareci ve istifadeci olub istifade muddeti qeyd edilmeyib obyekt yoxdur !")

                    
           
        except:
            print("Istifade muddetinin yoxlanmasinda xeta bas verdi !")


        try:      
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_tamad")
            arcpy.SelectLayerByAttribute_management("torpaq_tamad","NEW_SELECTION","SENEDNOVU IS NOT NULL AND FULL_NAME IS NULL")
            arcpy.MakeFeatureLayer_management("torpaq_tamad","torpaq_tamad2")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_tamad2"))

               
          
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_tamad2",self.output+"\Senednovu_var_Tam_adi_yoxdur","INSIDE")

                print("Sened novu var tam adi qeyd edilmeyib, xetalara gonderildi !")

            else:
                print("Sened novu olanlarin tam adi qeyd edilib !")

                    
           
        except:
            print("Sened novu olub tam adi olmayan parsellerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_leqal_Y")
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili_leqal_Y")
            arcpy.SelectLayerByAttribute_management("torpaq_leqal_Y","NEW_SELECTION","LEQAL_MI=0")
            arcpy.MakeFeatureLayer_management("torpaq_leqal_Y","torpaq_leqal_Y2")
            arcpy.SelectLayerByAttribute_management("tikili_leqal_Y","NEW_SELECTION","LEQAL_MI=1 AND SENEDNOVU IS NULL AND SENEDSEKIL IS NULL")
            arcpy.MakeFeatureLayer_management("tikili_leqal_Y","tikili_leqal_Y2")
            arcpy.SelectLayerByLocation_management("tikili_leqal_Y2","WITHIN","torpaq_leqal_Y2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili_leqal_Y2","tikili_leqal_Y3")

            count_torpaq_atribut = str(arcpy.GetCount_management("tikili_leqal_Y3"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili_leqal_Y3",self.output+"\Torpaq_leqal_deyil_tikili_leqal_senedi_yox","INSIDE")

                print("Tikilisi leqal olub torpagi qeyri leqal olan obyektler xetalara gonderildi !")

        
        except:
            print("Tikilisi leqal olub torpagi qeyri leqal olan obyektlerin yoxlanmasinda xeta bas verdi !")












    def delete_empty_feature(self):
        ############## Xetalar ucun secilmis bazaya gonderilen bos laylar databazadan silinir ###################
        try:
            self.list_feature  = arcpy.arcpy.ListFeatureClasses("*")
            for self.fc in self.list_feature:
                self.count_obj = str(arcpy.GetCount_management(self.fc))
                if self.count_obj == "0":
                    arcpy.Delete_management(self.fc)

            print("Bos olan laylar silindi !")


        except:
            print("Bos olan laylarin silinmesinde xeta bas verdi !")







checkdata = Check_Database()
