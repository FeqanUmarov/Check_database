import arcpy
from arcpy import env
import os
class Check_Database():
    
    while True:
        try:
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
            output = input("Xetalarin gonderileceyi bazani daxil et:")
            if output!="":
                break

            else:
                print("Xetalarin gonderileceyi yeri daxil edin!")
                continue

        except:
            print("Xetalarin gonderileceyi yer teyin edilmeyib!")
    env.workspace = database
    arcpy.env.overwriteOutput = True

    def __init__(self):
        
        self.about_app()

    def about_app(self):
        print("""Cografi verilenler bazasinin yoxlanilmasi sistemine xos gelmisiniz! "check_feature"-verilenler bazasinda olan laylarin adlarinin standarta uygun olmasini yoxla
        (eger laylarin adi standart olmasa diger proseslerde xetalarla qarsilasa bilerik) """)

    def check_feature(self):
        try:
        
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
            arcpy.CreateTopology_management(self.database,"Topology")
            self.fcList = arcpy.ListFeatureClasses()
            for self.fcname in self.fcList:
                if self.fcname == "KOMEKCI" or "TORPAQ_TUM" or "TIKILI_TUM" or "SEKTOR" or "QUARTER":
                    arcpy.AddFeatureClassToTopology_management("Topology",self.fcname)
                    
            arcpy.AddRuleToTopology_management("Topology","Must Not Overlap With (Area-Area)",self.database+'\KOMEKCI',"",self.database+'\TIKILI_TUM',"")
            arcpy.AddRuleToTopology_management("Topology","Must Not Overlap (Area)",self.database+'\TORPAQ_TUM',"","")
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

            print("************************************************************************************************")
            print("Prosesler zamani yaranmis elave laylar databazadan ugurla silindi!...")
            print("************************************************************************************************")

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Elave laylarin silinmesi prosesinde xeta bas verdi!")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        
    def check_field_value_full(self):
        print("Atribut melumatlarinin tam doldurulmasi yoxlanilir...")
        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","EMLAK_NOVU is null")
            arcpy.MakeFeatureLayer_management("torpaq","process")
            count_torpaq = str(arcpy.GetCount_management("process"))

            if count_torpaq!="0":
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
                print("SECTOR_NAME sutununda bos olan melumat var!")

            else:
                print("SECTOR_NAME sutununda bos olan melumat yoxdur!")

        except:
            print("SECTOR_NAME sutununun dolu olub olmamasinin yoxlanilmasi prosesinde xeta bas verdi! Sutun adi standarta uygun deyil!")

    def check_atribute(self):
        print("Atribut melumatlari yoxlanilir...")
        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_emlak","(EMLAK_NOVU = 0 AND ALT_IST_NOVU NOT IN(1,3,5,7,10,11,12,13,20,21,22,25,27,31,32,42,51,53,61,62,63,66,67,77,80,82,91,94,95,97,98,99,100,101,102,103,105,107,109,110,113,117,118,123,124,126,130,135,137,138,139,146,149,151,152,153,159,160,161,115)) OR (EMLAK_NOVU =1 AND ALT_IST_NOVU NOT IN (0,2,6,8,15,26,35,39,44,119,128,129,131,132)) OR (EMLAK_NOVU =3 AND ALT_IST_NOVU NOT IN(17,18,81,121,140,145)) OR  (EMLAK_NOVU = 9 AND ALT_IST_NOVU NOT IN(38)) OR (EMLAK_NOVU = 4 AND ALT_IST_NOVU NOT IN( 19 )) OR (EMLAK_NOVU = 11 AND ALT_IST_NOVU NOT IN(16,30,36,41,50,55,65,68,89,90,96,111,122,136,141,143,144,158,162)) OR (EMLAK_NOVU = 13 AND ALT_IST_NOVU NOT IN(23,64,106,154,155,156,157)) OR (EMLAK_NOVU = 2 AND ALT_IST_NOVU NOT IN(56,74,75,76,78,79,87,104,112)) OR (EMLAK_NOVU =12 AND ALT_IST_NOVU NOT IN(9,86,114,125)) OR (EMLAK_NOVU = 6 AND ALT_IST_NOVU NOT IN(14,29,33,34,43,54,84,85,120,127)) OR (EMLAK_NOVU =14 AND ALT_IST_NOVU NOT IN(37,52,69))")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_emlak"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_emlak",self.output+"\Emlak_novu_uqodiyasi_arasinda_uygunsuzluq")
                print("Emlak novu ile uqodiya arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Emlak novu ile uqodiya arasinda uygunsuzluq yoxdur!")
        except:
            print("Emlak novu ile uqodiyanin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_kateqoriya","(T_KATEGORI = 0 AND ALT_KATEGORI NOT IN(0,1,2,3,4)) OR (T_KATEGORI = 1 AND ALT_KATEGORI NOT IN(5,6,7)) OR (T_KATEGORI =2 AND ALT_KATEGORI NOT IN(8,9,10,11,12)) OR (T_KATEGORI =3 AND ALT_KATEGORI NOT IN(18,19,20,21,22)) OR (T_KATEGORI =4 AND ALT_KATEGORI NOT IN(13)) OR (T_KATEGORI =6 AND ALT_KATEGORI NOT IN(23)) OR ( T_KATEGORI = 5 AND ALT_KATEGORI NOT IN(14,15,16,17) )")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_kateqoriya"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_kateqoriya",self.output+"\Kateqoriyasi_alt_kateqoriyasi_arasinda_uygunsuzluq")
                print("Kateqoriya ile alt kateqoriya arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Kateqoriya ile alt kateqoriya arasinda uygunsuzluq yoxdur!")
        except:
            print("Kateqoriya ile alt kateqoriya yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_altkateqoriya","(ALT_KATEGORI = 5 AND ALT_IST_NOVU NOT IN( 0 ,12,17,18,31,32,38,42,51,81,121,135,140,145)) OR (ALT_KATEGORI = 6  AND ALT_IST_NOVU NOT IN(1,3,4,9,14,16,24,25,29,30,33,34,36,37,40,41,43,44,45,46,47,48,49,50,52,54,55,58,59,60,65,68,69,70,71,72,82,83,84,85,86,88,89,90,92,93,96,108,111,114,120,122,125,127,133,134,136,137,139,141,142,143,144,147,149,150,152,158,162)) OR (ALT_KATEGORI = 7  AND ALT_IST_NOVU NOT IN(2,5,6,7,8,10,11,13,15,19,20,21,22,23,26,27,28,35,39,53,56,57,61,62,63,64,66,67,73,74,75,76,77,78,79,80,87,91,94,95,97,98,99,100,101,102,103,104,105,106,107,109,110,112,113,116,117,118,119,123,124,126,128,129,130,131,132,138,146,151,153,154,155,156,157,159,160))")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_altkateqoriya"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_altkateqoriya",self.output+"\Alt_kateqoriya_uqodiya_arasinda_ferq")
                print("Alt kateqoriya ile alt istifade novu arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Alt kateqoriya ile alt istifade novu arasinda uygunsuzluq yoxdur!")
        except:
            print("Alt kateqoriya ile alt istifade novu yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq_mulkreyestr","(mid ([REYESTR_NO],6,1) ='3' AND [MULKFORM] <>2) OR (mid ([REYESTR_NO],6,1) <> '3' AND [MULKFORM] =2) OR (mid ([REYESTR_NO],6,1) ='2' AND [MULKFORM] <>1) OR (mid ([REYESTR_NO],6,1) <>'2' AND [MULKFORM] =1) OR (mid ([REYESTR_NO],6,1) ='1' AND [MULKFORM] <>0) OR (mid ([REYESTR_NO],6,1) <> '1' AND [MULKFORM]=0)")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq_mulkreyestr"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq_mulkreyestr",self.output+"\Mulkiyyeti_ile_reyestr_nomresi_arasinda_uygunsuzluqlar")
                print("Mulkiyyet ile reyestr nomresi arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Mulkiyyet ile reyestr nomresi arasinda uygunsuzluq yoxdur!")
        except:
            print("Mulkiyyet ile reyestr nomresi yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","altkateqoriyamulkiyyet","[ALT_KATEGORI] = 7 AND [MULKFORM] = 2")
            count_torpaq_atribut = str(arcpy.GetCount_management("altkateqoriyamulkiyyet"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("altkateqoriyamulkiyyet",self.output+"\Alt_kateqoriyasi_umumi_istifade_mulkiyyeti_xususidir")
                print("Alt kateqoriya ile mulkiyyet arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Alt kateqoriya ile mulkiyyet arasinda uygunsuzluq yoxdur!")
        except:
            print("Alt kateqoriya ile mulkiyyet yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","kateqoriyamulkiyyet","T_KATEGORI IN(4,5) AND MULKFORM =2")
            count_torpaq_atribut = str(arcpy.GetCount_management("kateqoriyamulkiyyet"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("kateqoriyamulkiyyet",self.output+"\Kateqoriyasi_mese_ve_su_fondu_mulkiyyet_xususi")
                print("Kateqoriya ile mulkiyyet arasinda olan uygunsuzluqlar askarlandi ve xetalar qovluguna gonderildi!")

            else:
                print("Kateqoriya ile mulkiyyet arasinda uygunsuzluq yoxdur!")
        except:
            print("Kateqoriya ile mulkiyyet yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senedsekilsenednov","SENEDSEKIL IS NOT NULL AND SENEDNOVU IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("senedsekilsenednov"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senedsekilsenednov",self.output+"\Senedsekili_var_senednovu_yoxdur")
                print("Sened sekili var, lakin sened novu yoxdur! Xetalara gonderildi...")

            else:
                print("Sened sekili ile sened novu arasinda uygunsuzluq yoxdur!")
        except:
            print("Sened sekili ile sened novunun yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","reyestrsened","REYESTR_NO IS NOT NULL AND SENEDNOVU IS NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("reyestrsened"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("reyestrsened",self.output+"\Reyestr_nomresi_var_senednovu_sahesi_yoxdur")
                print("Reyestr nomresi var lakin sened novu ve sahesi yoxdur! Xetalara gonderildi...")

            else:
                print("Reyestr ile sened novu ve sahe arasinda uygunsuzluq askarlanmadi!")
        except:
            print("Reyestr ile sened novu sahenin yoxlanmas prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senednovuleqalliq","T_KATEGORI = 1 AND SENEDNOVU IN(7,10,11,12,13) AND LEQAL_MI = 0")
            count_torpaq_atribut = str(arcpy.GetCount_management("senednovuleqalliq"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senednovuleqalliq",self.output+"\Senednovu_var_legalligi_xeyr")
                print("Sened novu var lakin leqalligi xeyr qeyd edilib! Xetalara gonderildi...")

            else:
                print("Sened novu ile leqalliq arasinda xeta askarlanmadi!")
        except:
            print("Sened novu ile leqalligin yoxlanilmasi prosesinde xeta bas verdi!")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senednovsekil","SENEDNOVU IS NOT NULL AND SENEDSEKIL IS NOT NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("senednovsekil"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senednovsekil",self.output+"\Senednovu_senedsekili_var_sahesi_yoxdur")
                print("Sened novu, senedsekili var sahesi yoxdur! Xetalara gonderildi...")

            else:
                print("Sened novu ile sahesi arasinda uygunsuzluq askarlanmadi!")
        except:
            print("Sened novu senedsekili ve sahenin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","reyestrnomresistandart","Len( REYESTR_NO) <>12 AND Len( REYESTR_NO) <>18")
            count_torpaq_atribut = str(arcpy.GetCount_management("reyestrnomresistandart"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("reyestrnomresistandart",self.output+"\Reyestr_nomreleri_standart_deyil")
                print("Reyestr nomresi standart deyil! Xetalara gonderildi...")

            else:
                print("Qeyri standart reyestr nomresi askarlanmadi !")
        except:
            print("Reyestr nomresinin standartliginin yoxlanilmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","senednovsenedsekilreyestr","SENEDNOVU IN(10,12) AND SENEDSEKIL IS NOT NULL AND REYESTR_NO IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("senednovsenedsekilreyestr"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("senednovsenedsekilreyestr",self.output+"\senednovu_senedsekili_var_reyestri_yoxdur")
                print("Sened novu var sened sekili var reyestr yoxdu! Xetalara gonderildi...")

            else:
                print("Sened novu sened sekili olanlarin reyestr var !")
        except:
            print("Sene novu sened sekili olanlarin reyestrinin yoxlanmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","reyestrleqalliq","REYESTR_NO IS NOT NULL AND LEQAL_MI = 0")
            count_torpaq_atribut = str(arcpy.GetCount_management("reyestrleqalliq"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("reyestrleqalliq",self.output+"\Reyestr_nomresi_var_legalligi_xeyr")
                print("Reyestr nomresi var leqalligi xeyir qeyd edilib! Xetalara gonderildi...")

            else:
                print("Reyestr olub leqalligi xeyr qeyd edilen obyekt yoxdur !")
        except:
            print("Reyestr ile leqalligin yoxlanilmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","dovmulkiyyet","MULKFORM = 0 AND LEQAL_MI = 0 AND ISTIFADE = 0")
            count_torpaq_atribut = str(arcpy.GetCount_management("dovmulkiyyet"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("dovmulkiyyet",self.output+"\Dovlet_mulkiyyeti_olub_legalligi_xeyr_olanlar")
                print("Dovlet mulkiyyetidir leqalligi xeyr qeyd edilib ! Xetalara gonderildi...")

            else:
                print("Dovlet mulkiyyeti olub leqalligi xeyr qeyd edilen parseller yoxdur !")
        except:
            print("Dovlet mulkiyyeti ile leqalligin yoxlanilmasi prosesinde xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","belediyyeistifade","MULKFORM = 1 AND ISTIFADE = 2 AND LEQAL_MI = 1 AND SENEDNOVU IS NULL AND SENEDSEKIL IS NULL AND REYESTR_NO IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("belediyyeistifade"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("belediyyeistifade",self.output+"\Mukiyyeti_belediyye_istifadeci_olub_senednovu_senedsekili_reyestri_olmayan_lakin_leqal_olan")
                print("Mulkiyyeti belediyyedir sened novu sened sekili ve reyestr yoxdur lakin leqalligi beli qeyd edilib ! Xetalara gonderildi...")

            else:
                print("Mulkiyyeti belediyyedir sened novu sened sekili ve reyestr yoxdur lakin leqalligi beli qeyd edilen obyektler movcud deyil !")
        except:
            print("Belediyye mulkiyyeti olub senedi olmayib leqalligi beli olan obyektlerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.SelectLayerByAttribute_management("tikili","NEW_SELECTION","TIKILI_NOVU = 16")
            arcpy.FeatureToPoint_management("tikili",self.output+"\point_building")
            
            arcpy.MakeFeatureLayer_management(self.output+"\point_building","tikili_noqte")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByLocation_management("torpaq","INTERSECT","tikili_noqte","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("torpaq","torpaq2")
           
            arcpy.SelectLayerByAttribute_management("torpaq2","NEW_SELECTION","EMLAK_NOVU=9")
            arcpy.SelectLayerByAttribute_management("torpaq2","SWITCH_SELECTION","")
            arcpy.MakeFeatureLayer_management("torpaq2","torpaq3")
            count_torpaq_atribut = str(arcpy.GetCount_management("torpaq3"))
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("torpaq2",self.output+"\orpaq_ferqli")


                print("Tikilisi ferdi yasayis olub torpaginin emlak novu ferdi yasayis olmayanlar xeta kimi gonderildi !")
           
        except:
            print("Tikilisi ferdi yasayis torpagi ferqli olan parselin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","MULKFORM=2")
            arcpy.MakeFeatureLayer_management("torpaq","torpaq2")
            arcpy.SelectLayerByLocation_management("tikili","WITHIN","torpaq2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            arcpy.SelectLayerByAttribute_management("tikili2","NEW_SELECTION","MULKFORM<>2")
            arcpy.MakeFeatureLayer_management("tikili2","tikili3")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili3"))
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Torpagi_xususi_tikilisi_ferqli")

                print("Torpaq xususi olub tikilisi ferqli olan obyektler xetalara gonderildi !")



            
           
        except:
            print("Torpaq xususi olub tikilisi ferqli olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili")
            arcpy.MakeFeatureLayer_management("TORPAQ_TUM","torpaq")
            arcpy.SelectLayerByAttribute_management("torpaq","NEW_SELECTION","EMLAK_NOVU=4")
            arcpy.MakeFeatureLayer_management("torpaq","torpaq2")
            arcpy.SelectLayerByLocation_management("tikili","WITHIN","torpaq2","","","NOT_INVERT")
            arcpy.MakeFeatureLayer_management("tikili","tikili2")
            arcpy.SelectLayerByAttribute_management("tikili2","NEW_SELECTION","TIKILI_NOVU=16")
            arcpy.MakeFeatureLayer_management("tikili2","tikili3")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili3"))
            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili2",self.output+"\Torpagi_xususi_tikilisi_ferqli")

                print("Torpaq coxmertebeli tikilisi ferdi yasayis olan obyektler xetalara gonderildi !")



            
           
        except:
            print("Torpaq coxmertebeli tikilisi ferdi yasayis olan obyektlerin yoxlanmasinda xeta bas verdi !")


        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili","SENEDSEKIL IS NOT NULL AND SENEDNOVU IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili",self.output+"\Senedsekili_var_Sened_Novu_Yoxdur_tikili")

                print("Sened sekili olub sened novu olmayan obyektler askarlanaraq xetalara gonderildi !")

            else:
                print("Sened sekili olub sened novu olmayan obyektler yoxdur")

                        
           
        except:
            print("Sened sekili olub sened novu olmayan obyektlerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili","REYESTR_NO IS NOT NULL AND SENEDNOVU IS NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili",self.output+"\Reyestri_var_senednovu_sahesi_yoxdur_tikili")

                print("Reyestri olub sened novu ve sahesi olmayan tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Reyestri olub sened novu ve sahesi olmayan tikililer yoxdur")

                        
           
        except:
            print("Reyestri olub sened novu ve sahesi olmayan tikililerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili","REYESTR_NO IS NOT NULL AND SAHE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili",self.output+"\Reyestri_var_sahesi_yoxdur_tikili")

                print("Reyestri olub sahesi olmayan tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Reyestri olub sahesi olmayan tikililer yoxdur")

                        
           
        except:
            print("Reyestri olub sahesi olmayan tikililerin yoxlanmasinda xeta bas verdi !")

        try:
            arcpy.MakeFeatureLayer_management("TIKILI_TUM","tikili","YARIMCIQ=0 AND MERTEBE IS NULL")
            count_torpaq_atribut = str(arcpy.GetCount_management("tikili"))

            if count_torpaq_atribut!="0":
                arcpy.FeatureToPoint_management("tikili",self.output+"\Tikili_yarimciq_deyil_mertebesi_qeyd_edilmeyib")

                print("Yarimciq olmayib lakin mertebesi qeyd edilmeyen tikililer askarlanaraq xetalara gonderildi !")

            else:
                print("Yarimciq olmayib mertebesi qeyd edilmeyen tikili askarlanmadi")

                        
           
        except:
            print("Yarimciq olmayib mertebesi qeyd edilmeyen tikililerin yoxlanmasinda xeta bas verdi !")

        




check = Check_Database()
