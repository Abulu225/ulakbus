# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
#

from zengine.forms import JsonForm, fields
from zengine.views.crud import CrudView
from collections import OrderedDict
from ulakbus.services.zato_wrapper import DersProgramiOlustur
from ulakbus.models import Room, Okutman, DersEtkinligi, Donem

ARAMA_TURU = [
    (1, 'Derslik'),
    (2, 'Öğretim Elemanı')
]


class AramaForm(JsonForm):
    class Meta:
        title = 'Öğretim Elemanı veya Derslik Ara'

    arama_sec = fields.String('Arama Seçeneği', choices=ARAMA_TURU, default=1)
    arama_text = fields.String(" ")
    arama_button = fields.Button('Ara')
    vazgec_button = fields.Button('Geri', cmd='vazgec')


class DersProgramiYap(CrudView):
    def ders_etkinligi_sayisi(self):
        ders_etkinligi_count = DersEtkinligi.objects.filter(bolum=self.current.role.unit,
                                                            donem=Donem.guncel_donem()).count()

        solved_count = DersEtkinligi.objects.filter(bolum=self.current.role.unit,
                                                    donem=Donem.guncel_donem(),
                                                    solved=True).count()

        published_count = DersEtkinligi.objects.filter(bolum=self.current.role.unit, published=True,
                                                       donem=Donem.guncel_donem()).count()

        return ders_etkinligi_count, solved_count, published_count

    def kontrol(self):
        ders_etkinligi_count, solved_count, published_count = self.ders_etkinligi_sayisi()

        if published_count > 0:
            self.current.task_data['cmd'] = 'kayit_var'

        elif solved_count == ders_etkinligi_count and solved_count > 0:
            self.current.task_data['cmd'] = 'hatasiz_sonuc'
            msg = {"type": 'info',
                   "title": 'Yayınlanmamış Ders Programı Var!',
                   "msg": 'Yayınlanmayan ders programını inceleyip yayınlayabilirsiniz.'}
            self.current.task_data['LANE_CHANGE_MSG'] = msg
        elif solved_count != ders_etkinligi_count and solved_count > 0:
            msg = {"type": 'warning',
                   "title": 'Hatalı Sonuçlar Var!',
                   "msg": 'Oluşturulan ders programınızda hatalı sonuçlar bulunmaktadır.'
                          'Lütfen tekrardan ders programı oluşturunuz.'}
            self.current.task_data['LANE_CHANGE_MSG'] = msg

    def ders_programi_hesaplama_baslat(self):
        if 'LANE_CHANGE_MSG' in self.current.task_data:
            if self.current.task_data['LANE_CHANGE_MSG']['title'] == 'Hatalı Sonuçlar Var!':
                self.current.output['msgbox'] = self.current.task_data['LANE_CHANGE_MSG']
        else:
            _form = JsonForm(title="Ders Programı Oluştur")
            _form.button = fields.Button('Başlat')
            self.form_out(_form)

    def ders_programi_hesapla(self):
        dp = DersProgramiOlustur(service_payload={"bolum": self.current.role.unit.yoksis_no,
                                                  "kullanici": self.current.user.key,
                                                  "url": self.current.get_wf_link()})
        response = dp.zato_request()

        if response:
            msg = {"type": 'info',
                   "title": 'Ders Programı Oluşturuluyor',
                   "msg": 'Ders programı için yaptığınız taleb başarıyla alınmıştır.'}
            self.current.task_data['LANE_CHANGE_MSG'] = msg
        else:
            msg = {"type": 'warning',
                   "title": 'Sistemde Sorun Oluştu',
                   "msg": 'Lütfen tekrardan ders programı oluşturmayı çalıştırnız!'}
            self.current.task_data['LANE_CHANGE_MSG'] = msg

    def servis_bilgi_mesaji(self):

        if self.current.task_data['LANE_CHANGE_MSG']['title'] == 'Ders Programı Oluşturuluyor':
            self.current.output['msgbox'] = self.current.task_data['LANE_CHANGE_MSG']
        else:
            self.current.output['msgbox'] = self.current.task_data['LANE_CHANGE_MSG']

    def ders_programi_sonucu(self):
        ders_etkinligi_count, solved_count, published_count = self.ders_etkinligi_sayisi()
        if solved_count != ders_etkinligi_count:
            msg = {"type": 'warning',
                   "title": 'Hatalı Sonuçlar Var!',
                   "msg": 'Oluşturulan ders programınızda hatalı sonuçlar bulunmaktadır.'
                          'Lütfen tekrardan ders programı oluşturunuz.'}
            self.current.task_data['LANE_CHANGE_MSG'] = msg

            self.current.task_data['cmd'] = 'hata'
        else:
            msg = {"type": 'info',
                   "title": 'Ders Programı Başarıyla Oluşturuldu!',
                   "msg": 'Yayınlanmayan ders programını inceleyip yayınlayabilirsiniz.'}
            self.current.task_data['LANE_CHANGE_MSG'] = msg

    def hatasiz(self):
        _form = JsonForm(title="Derslik veya Öğretim Elemanı İncele")
        _form.incele = fields.Button("İncele", cmd='incele')
        _form.yayinla = fields.Button("Yayınla", cmd='bitir')
        self.form_out(_form)
        self.current.output['msgbox'] = self.current.task_data['LANE_CHANGE_MSG']

    def derslik_og_elemani_ara(self):

        self.form_out(AramaForm(self.object, current=self.current))

    def arama(self):
        text = str(self.input['form']['arama_text'])
        try:
            if self.input['form']['arama_sec'] == 1:
                room_search = [r for r in Room.objects.filter(code=text) if self.current.role.unit in r.RoomDepartments]
                if room_search:
                    self.current.task_data['data_key'] = room_search[0].key
                    self.current.task_data['cmd'] = 'tekli'
                else:
                    raise
            else:
                ad = text.split()[0]
                soyad = text.split()[1]
                okutman_search = Okutman.objects.filter(ad=ad, soyad=soyad)
                if len(okutman_search) > 1:
                    self.current.search = okutman_search
                    self.current.task_data['cmd'] = 'coklu'
                elif len(okutman_search) == 1:
                    self.current.task_data['data_key'] = okutman_search[0]
                    self.current.task_data['cmd'] = 'tekli'
                else:
                    raise
        except:
            msg = {
                'type': 'warning', "title": 'Kayıt Bulunamadı',
                "msg": 'İlgili kayıt bulunamadı.'
            }
            self.current.task_data["LANE_CHANGE_MSG"] = msg

    def coklu_sonuc(self):

        self.output['objects'] = [['Ad', 'Soyad']]
        for data in self.current.search:
            data_list = OrderedDict({})
            data_list['Ad'] = data.ad
            data_list['Soyad'] = data.soyad
            item = {
                'type': "table-multiRow",
                'fields': data_list,
                'actions': [
                    {'name': 'Goster', 'cmd': 'tek_sonuc', 'show_as': 'button', 'object_key': 'ogretim_elemani'}
                ],
                'key': data.key
            }
            self.output['objects'].append(item)

    def detay_goster(self):

        if "LANE_CHANGE_MSG" in self.current.task_data and \
                        self.current.task_data["LANE_CHANGE_MSG"]["title"] == "Kayıt Bulunamadı":
            self.current.output['msgbox'] = self.current.task_data["LANE_CHANGE_MSG"]
        else:
            if self.input['form']['arama_sec'] == 1:
                ders_etkinligi = sorted(DersEtkinligi.objects.filter(room_id=self.current.task_data['data_key']),
                                        key=lambda d: (d.gun, d.baslangic_saat, d.baslangic_dakika))
            else:
                ders_etkinligi = sorted(DersEtkinligi.objects.filter(
                    okutman_id=self.current.task_data['data_key']),
                    key=lambda d: (d.gun, d.baslangic_saat, d.baslangic_dakika))

            days = ["Saat Aralığı", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

            for data in ders_etkinligi:
                if self.input['form']['arama_sec'] == 1:
                    ad = data.okutman.ad
                    soyad = data.okutman.soyad
                else:
                    ad = data.room.code
                    soyad = data.room.name
                data_list = OrderedDict({})

                data_list["Saat Aralığı"] = "%s:%s-%s:%s" % (data.baslangic_saat,
                                                             data.baslangic_dakika,
                                                             data.bitis_saat,
                                                             data.bitis_dakika)
                for i in range(1, len(days)):
                    if data.gun == i:
                        data_list[days[i]] = "%s %s" % (ad, soyad)
                    else:
                        data_list[days[i]] = " "

                item = {
                    "title": "Detaylı Zaman Tablosu",
                    'type': "table-multiRow",
                    'fields': data_list}
                self.output['objects'].append(item)
        _json = JsonForm(title="Güncel Zaman Dilimleri")
        _json.tamamla = fields.Button("Bitir")
        self.form_out(_json)

    def hatali(self):
        msg = {"type": 'info',
               "title": 'Yayınlanmamış Ders Programı Var!',
               "msg": 'Yayınlanmayan ders programını inceleyip yayınlayabilirsiniz.'}
        self.current.task_data['LANE_CHANGE_MSG'] = msg

    def yayinla(self):
        des = DersEtkinligi.objects.filter(bolum=self.current.role.unit, donem=Donem.guncel_donem())
        for de in des:
            de.published = True
            de.save()

    def bilgilendirme(self):
        self.current.output['msgbox'] = self.current.task_data['LANE_CHANGE_MSG']


class OgretimElemaniDersProgrami(CrudView):

    def kontrol(self):
        okutman = Okutman.objects.get(personel=self.current.user.personel)
        ders_etkinligi = sorted(DersEtkinligi.objects.filter(okutman=okutman), key=lambda d: (d.gun, d.baslangic_saat))
        for de in ders_etkinligi:
            if not de.published or de.published is False:
                self.current.task_data['cmd'] = 'yok'
                break

    def ders_programini_goster(self):
        okutman = Okutman.objects.get(personel=self.current.user.personel)
        ders_etkinligi = sorted(DersEtkinligi.objects.filter(okutman=okutman), key=lambda d: (d.gun, d.baslangic_saat))

        dersler = list()

        for de in ders_etkinligi:
            ders = dict()
            ders['ad'] = de.sube.ders.ad
            ders['gun'] = de.gun
            ders[
                'saat_araligi'] = de.baslangic_saat + ':' + de.baslangic_dakika + '-' + de.bitis_saat + ':' + de.bitis_dakika
            dersler.append(ders)
        item = {'read_only': True,
                'name': self.current.user.name,
                'gunler': ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
                'dersler': dersler}

        self.output['ders_programi'] = item

    def ders_programi_bulunamadi(self):
        msg = {"type": "warning",
               "title": 'Ders Programı Bulunamadı',
               "msg": "Ders Programı Henüz Oluşturulmadı."}

        self.current.output['msgbox'] = msg
