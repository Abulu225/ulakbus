# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

from pyoko.model import Model, ListNode, Node
from pyoko import field


class Personel(Model):
    tckn = field.String("TC No", index=True)
    ad = field.String("Adı", index=True)
    soyad = field.String("Soyadı", index=True)
    personelTuru = field.String("Personel Türü", index=True)
    dogumTarihi = field.Date("Doğum Tarihi", index=True)
    cepTelefonu = field.String("Cep Telefonu", index=True)

    class NufusKayitlari(Node):
        tckn = field.String("Sigortalının TC Kimlik No", index=True)
        ad = field.String("Adi", index=True)
        soyad = field.String("Soyadi", index=True)
        ilkSoyAd = field.String("Memuriyete Girişteki İlk Soyadı", index=True)
        dogumTarihi = field.String("Dogum Tarihi", index=True)
        cinsiyet = field.String("Cinsiyet", index=True)
        emekliSicilNo = field.Integer("Emekli Sicil No", index=True)
        memuriyetBaslamaTarihi = field.String("Memuriyete Ilk Baslama Tarihi", index=True)
        kurumSicil = field.String("Kurum Sicili", index=True)
        maluliyetKod = field.String("Malul Kod", index=True)
        yetkiSeviyesi = field.String("Yetki Seviyesi", index=True)
        aciklama = field.String("Aciklama", index=True)
        kurumaBaslamaTarihi = field.String("Kuruma Baslama Tarihi", index=True)
        gorevTarihi6495 = field.String("Emeklilik Sonrası Göreve Başlama Tarihi", index=True)
        emekliSicil6495 = field.Integer("2. Emekli Sicil No", index=True)
        durum = field.String("Durum", index=True)
        sebep = field.Integer("Sebep", index=True)

    class AskerlikKayitlari(ListNode):
        askerlikNevi = field.Integer("Askerlik Nevi", index=True)
        baslamaTarihi = field.String("Başlama Tarihi", index=True)
        bitisTarihi = field.String("Bitiş Tarihi", index=True)
        kayitNo = field.Integer("Kayıt No", index=True)
        kitaBaslamaTarihi = field.String("Kıta Başlama Tarihi", index=True)
        kitaBitisTarihi = field.String("Kıta Bitiş Tarihi", index=True)
        muafiyetNeden = field.String("Muafiyet Neden", index=True)
        sayilmayanGunSayisi = field.Integer("Sayılmayan Gün Sayısı", index=True)
        sinifOkuluSicil = field.String("Sınıf Okulu Sicil", index=True)
        subayliktanErligeGecisTarihi = field.String("Subaylıktan Erliğe Geçiş Tarihi", index=True)
        subayOkuluGirisTarihi = field.String("Subay Okulu Giriş Tarihi", index=True)
        tckn = field.Integer("TC Kimlik No", index=True)
        tegmenNaspTarihi = field.String("Teğmen Nasp Tarihi", index=True)
        gorevYeri = field.String("Görev Yeri", index=True)
        kurumOnayTarihi = field.String("Kurum Onay Tarihi", index=True)
        astegmenNaspTarihi = field.String("Asteğmen Nasp Tarihi", index=True)


    class HizmetKayitlari(ListNode):
        tckn = field.String("Sigortalının TC Kimlik No", index=True)
        field.Integer("Kayıt Numarasi", index=True)
        baslamaTarihi = field.Date("Hizmet Başlama Tarihi", index=True, format="%d.%m.%Y")
        bitisTarihi = field.Date(" Hizmet Bitiş Tarihi", index=True, format="%d.%m.%Y")
        gorev = field.Integer("Görevi", index=True)
        unvanKod = field.Integer("Unvan Kod", index=True)
        yevmiye = field.String("Yevmiye", index=True)
        ucret = field.String("Ucret", index=True)
        hizmetSinifi = field.String("Hizmet Sinifi", index=True)
        kadroDerece = field.Integer("Kadro Derecesi", index=True)
        odemeDerece = field.Integer("Odeme Derece", index=True)
        odemeKademe = field.Integer("Odenen Kademe", index=True)
        odemeEkgosterge = field.Integer("Odeme Ekgosterge", index=True)
        kazanilmisHakAyligiDerece = field.Integer("Kazanilmis Hak Ayliginin Derece", index=True)
        kazanilmisHakAyligiKademe = field.Integer("Kazanilmis Hak Ayliginin Kademe", index=True)
        kazanilmisHakAyligiEkgosterge = field.Integer("Kazanilmis Hak Ayliginin Ekgosterge", index=True)
        emekliDerece = field.Integer("Emeklilige Esas Derece", index=True)
        emekliKademe = field.Integer("Emekli Esas Kademe", index=True)
        emekliEkgosterge = field.Integer("Emeklilige Esas Ekgosterge")
        sebepKod = field.Integer("Sebep Kod", index=True)
        kurumOnayTarihi = field.String("Kurum Onay Tarihi", index=True)

        class Kullanici(ListNode):
            id = field.Integer("Kullanıcının ID No", index=True)
            tckn = field.String("Kullanıcının TC Kimlik No", index=True)
            name = field.String("Kullanıcının Adı", index=True)
            surname = field.String("Kullanıcının Soyadı", index=True)
            birth_date = field.String("Kullanıcının Doğum Tarihi", index=True)
            birth_place = field.String("Kullanıcının Doğum Yeri", index=True)
            neighborhood = field.String("Kullanıcının Mahallesi", index=True)
            father_name = field.String("Kullanıcının Baba Adı", index=True)
            mother_name = field.String("Kullanıcının Anne Adı", index=True)
            gender = field.String("Kullanıcının Cinsiyeti", index=True)
            marital_status = field.String("Kullanıcının Medeni Durumu", index=True)
            town_code = field.Integer("Kullanıcının Şehir Kodu", index=True)
            city = field.Integer("Kullanıcının Yaşadığı Şehir", index=True)
            blood_type = field.String("Kullanıcının Kan Grubu", index=True)
            former_surname = field.String("Kullanıcının Eski Soyadı", index=True)
            home_phone = field.String("Kullanıcının Ev Telefonu", index=True)
            work_phone = field.String("Kullanıcının İş Telefonu", index=True)
            mobile_phone = field.String("Kullanıcının Cep Telefonu", index=True)
            address_sec = field.String("Kullanıcının Mahallesi", index=True)
            postal_code = field.String("Kullanıcının Mahallesi", index=True)
            primary_email = field.String("Kullanıcının Birinci Maili", index=True)
            secondary_email = field.String("Kullanıcının İkinci Maili", index=True)
            website = field.String("Kullanıcının Web Sitesi", index=True)

        class Yetki(ListNode):
            name = field.String("Yetki Adı", index=True)
            code= field.String("Yetki Kodu", index=True)





        '''
        suspension_date = field.Date("Açığa Alınma Tarihi", index=True)
        monthly_start_date = field.Date("Aylık Ödenen Süre Başlangı Tarihi", index=True)
        monthly_stop_date = field.Date("Aylık Ödenen Süre Bitis Tarihi", index=True)
        openly_designation_date = field.Date("Açıktan Atandığı Tarih", index=True)
        suspension = field.Integer("Açığa Alınma Şekli", index=True)
        first_name = field.String("Adı", index=True)
        reel_name = field.String("Asıl Ad(Eski Ad)", index=True)
        reel_birth_date = field.Date("Asıl Doğum Tarihi(Eski Doğum Tarihi)", index=True)
        reel_surname = field.String("Asıl Soyad(Eski Soyad)", index=True)
        reel_agent = field.String("Asıl Vekil", index=True)
        soldiery_type = field.Integer("ASkerlik Nevi", index=True)
        astegmen_nasip_date = field.Date("Asteğmenliğe Nasp Tarihi", index=True)
        appointment_type = field.String("Atama Sekli", index=True)
        quit_job_reason = field.String("SSK Hizmetinden Ayrılma Sebebi", index=True)
        quit_job_date = field.Date("Son Kurumdan Ayrılma Tarihi", index=True)
        bagkur_job = field.String("Bağkur Mesleki Faaliyeri", index=True)
        bank_chest_dode = field.Integer("Banka Sandık Kodu", index=True)
        start_date = field.Date("Başlangıç Tarihi", index=True, format="%d.%m.%Y")
        start_date_debt = field.Date("Borçlanma Başlangıç Tarihi", index=True)
        end_date = field.Date("Bitiş Tarihi", index=True, format="%d.%m.%Y")
        end_date_debt = field.Date("Borçlanma Bitiş Tarihi", index=True)
        graduation_department = field.String("Mezun Olunan Bölüm", index=True)
        department_name = field.String("Varsa bölüm adı", index=True)
        establisment_date = field.Date("Tahakkuk Tarihi", index=True)
        debt_type = field.String("Borç Nevi", index=True)
        work_place = field.String("Borçlandığı Tarihte Çalıştığı Kurum", index=True)
        equivalent_department = field.String("Denklik Alınan Bölümün Adı", index=True)
        equivalent_school = field.String("Denklik Alınan Okulun Adı", index=True)
        equivalent_date = field.Date("Denklik Tarihi", index=True)
        degree = field.Integer("Borçlanmaya Esas Derece", index=True)
        return_status = field.Integer("İade Şekli/Nedeni", index=True)
        status_code = field.Integer("Sigortalının Son Durumu", index=True)
        status_explanation = field.String("Durum Kodu Açıklaması", index=True)
        indicator = field.Integer("Borçlanmaya Esas Ek Gösterge", index=True)
        retirement_degree = field.Integer("Emeklilik Derece", index=True)
        retirement_grade = field.Integer("Emeklilik Kademe", index=True)
        retirement_indicator = field.Float("Emeklilik Gösterge", index=True)
        retirement_registry = field.String("Sigortalının Emeklilik Sicil Numarası", index=True)
        fhz_ratio = field.Float("Unvana İlişkin FHZ katsayısı", index=True)
        valid_birth_date = field.Date("Emeklilikte Geçerli Doğum Tarihi", index=True)
        duty_unit = field.String("Görev Yaptığı Yer/Birim")
        assignment = field.String("Görev", index_as='text_tr')
        duty = field.Integer("Sigortalının Görev Tazminatı Göst", index=True)
        duty_return_request_date = field.Date("Göreve İade İsteminde Bulunduğu Tarih", index=True)
        duty_return_date = field.Date("Göreve İade Edildiği Tarih", index=True)
        duty_last_month_start_date = field.Date("Göreve Son Aylık Başlama Tarihi", index=True)
        duty_last_month_end_date = field.Date("Göreve Son Aylık Bitis Tarihi", index=True)
        duty_end_date = field.Date("Görevine Son Verildiği Tarih", index=True)
        number_of_days = field.Integer("İntibakta değerlendirilen Gun Sayısı", index=True)
        number_of_days_debt = field.Integer("Borçlanılan Gün Sayısı", index=True)
        motion_reason_code = field.Integer("Sigortalının Mevcut Hareket Kodu", index=True)
        motion_reason_explanation = field.String("Hareket Sebep Kod Açıklaması", index=True)
        prep_class = field.Integer("Hazırlık Sınıfı", index=True)
        duty_status = field.Integer("Hizmet Alma Durumu", index=True)
        duty_class = field.String("Hizmet Sınıfı", index=True)
        case = field.String("Husus", index=True)
        ihz_type = field.Integer("İHZ Nevi", index=True)
        work_place_country = field.String("Kurum İl", index=True)
        work_place_district = field.String("Kurum İlçe", index=True)
        grade = field.Integer("Borçlanmaya Esas Kademe", index=True)
        position_degree = field.String("Kadro Derece", index_as='text_tr')
        not_on_the_permanent_staff = field.Integer("Sigortalının kadrosuzluk Tazminat Oranı", index=True)
        ssk_kamu_workspace_name = field.String("Kamuda Çalıştığı SSK İşyeri Adı", index=True)
        law_code = field.Integer("Kanun Numarası", index=True)
        judgment_date = field.Date("Mahkeme Karar Tarihi", index=True)
        judgment_count = field.Integer("Mahkeme Karar Sayısı", index=True)
        judgment_confirmation_date = field.Date("Karar Kesinleştirme Tarihi", index=True)
        record_id = field.Integer("Kayıt No", index=True)
        aquired_degree = field.Integer("Kazanılmış Hak Aylığı Derece", index=True)
        aquired_grade = field.Integer("Kazanılmış Hak Aylığı Kademe", index=True)
        aquired_sup_indicator = field.Float("Kazanılmış Hak Aylığı Ek gösterge", index=True)
        kha_status = field.String("KHA durumu", index=True)
        severance_pay_status = field.Integer("Kıdem Tazminatı Ödeme Durumu", index=True)
        continent_start_date = field.Date("Kıta Hizmeti Başlama Tarihi", index=True)
        continent_end_date = field.Date("Kıta Hizmeti Bitiş Tarihi", index=True)
        course_type = field.Integer("Kurs Türü", index=True)
        period_of_study = field.Integer("Kurs Süresi", index=True)
        approval_date = field.Date("Kurum Onay Tarihi", index=True)
        court_name = field.String("Kararın Verildiği Mahkemenin Adi", index=True)
        position = field.Integer("Sigortalının Makam Tazminatı Göst", index=True)
        graduation_date = field.Date("Mezuniyet Tarihi", index=True)
        extemption_reason = field.String("Askerlikten Muafiyet Nedeni", index=True)
        pay_degree = field.Integer("Ödemeye Esas Derece", index=True)
        pay_sup_indicator = field.Float("Ödeme Ek Gösterge", index=True)
        pay_grade = field.Integer("Ödemeye Esas Kademe", index=True)
        pay_date = field.Date("Odeme Tarihi", index=True)
        be_paid_price = field.Float("Ödenen Tutar", index=True)
        learning_status = field.Integer("OGrenim Durumu", index=True)
        learning_period = field.Integer("Okul Süresi(Başarılı Öğrenim Süresi", index=True)
        learning_place = field.String("Öğrenim Yeri", index=True)
        school_name = field.String("Okul Adı/ Kurs Eğitim Yeri", index=True)
        ssk_ozel_workspace_name = field.String("Özelde Çalıştığı SSK İş Yeri Adı", index=True)
        uncounted_days = field.Integer("Askerlikten Sayılmayan Gun Sayisi", index=True)
        reason_code = field.Integer("Sebep Kodu", index=True)
        class_school_registry = field.String("Sınıfı, Dönemi, Sicili", index=True)
        sgk_type = field.Integer("Sgk Nevi", index=True)
        sgk_registry_no = field.String("Sosyal Güvenlik Numarası", index=True)
        result_code = field.Integer("Sorgulamanın Sonucunu Belirten Kod", index=True)
        result_message = field.String("Sonuc Kodunun Açıklanması", index=True)
        subayliktan_erlige_transfered_date = field.Date("Yedek Subaylıktan Erliğe veya Erlikten Yedek Subaylığa Geçiş Tarihi", index=True)
        subay_entered_date = field.Date("Yedek Subay Okuluna Giriş Tarihi", index=True)
        period = field.Integer("Prim Gün Sayısı", index=True)
        state_of_siege_remove_date = field.Date("Sıkı Yönetimin İlde Kaldırıldığı Tarih", index=True)
        correction_name = field.String("Tashih Adı(Yeni Ad)", index=True)
        correction_birth_date = field.Date("Tashih Doğum Tarihi(Yeni Doğum Tarihi)", index=True)
        correction_surname = field.String("Tashih Soyadı(Yeni Soyad)", index=True)
        compensation_date = field.Date("Sigortalının Tazminat Başlama Tarihi", index=True)
        pno = field.String("Sigortalının TC Kimlik No", index=True)
        compensation_end_date = field.Date("Sigortalını Tazminat Bitiş Tarihi", index=True)
        tegmen_nasp_date = field.String("Teğmenliğe Nasp Tarihi", index=True)
        representation = field.Integer("Sigortalının Temsil Tazminatı Göst", index=True)
        total_price = field.Float("Toplam Borç Tutarı", index=True)
        salary = field.String("Ücret", index=True)
        country_code = field.Integer("Ülke Kodu", index=True)
        title_code = field.Integer("Ünvan Kodu", index=True)
        title_date = field.Date("Ünvan Aldığı Tarih", index=True)
        title_end_date = field.Date("Ünvanın Sona Erdiği Tarih", index=True)
        yedek_subay_er_ogrenim_yer = field.String("Yedek Subay/ Er Öğrt Görev Yeri", index=True)
        authorisation_explanation = field.String("Yetki Kodu Açıklaması", index=True)
        authorisation_code = field.Integer("Yetki Kodu", index=True)
        wage = field.String("Yemiye", index=True)
        '''
