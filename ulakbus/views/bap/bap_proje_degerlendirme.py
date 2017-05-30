# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from ulakbus.models import BAPProje, Personel, User
from zengine.forms import JsonForm
from zengine.views.crud import CrudView
from zengine.lib.translation import gettext as _, gettext_lazy as __
from zengine.forms import fields

from pyoko import field


class ProjeDegerlendirmeForm(JsonForm):
    class Meta:
        title = _(u"Bilimsel Araştırma Projesi (BAP) Proje Başvuru Değerlendirme Formu")
        # always_blank = False

        grouping = [
            {
                "layout": "6",
                "groups": [
                    {

                        "items": ['arastirma_kapsam_tutar', 'arastirma_kapsam_tutar_gerekce',
                                  'literatur_ozeti', 'literatur_ozeti_gerekce', 'ozgun_deger',
                                  'ozgun_deger_gerekce', 'yontem_amac_tutar',
                                  'yontem_amac_tutar_gerekce', 'yontem_uygulanabilirlik',
                                  'yontem_uygulanabilirlik_gerekce']

                    }
                ]
            },
            {
                "layout": "6",
                "groups": [
                    {

                        "items": ['katki_beklenti', 'katki_beklenti_gerekce',
                                  'bilim_endustri_katki', 'bilim_endustri_katki_gerekce',
                                  'arastirmaci_bilgi_yeterlilik',
                                  'arastirmaci_bilgi_yeterlilik_gerekce',
                                  'butce_gorus_oneri', 'basari_olcut_gercek',
                                  'basari_olcut_gercek_gerekce', 'proje_gorus_oneri']
                    }
                ]
            },
            {
                "layout": "12",
                "groups": [
                    {

                        "items": ['proje_degerlendirme_sonucu']
                    }
                ]
            }
        ]

    arastirma_kapsam_tutar = field.Integer(_(u"ARAŞTIRMA KAPSAMININ PROJE AMACI İLE TUTARLILIĞI"),
                                           choices='bap_proje_degerlendirme_secenekler',
                                           default=1)
    arastirma_kapsam_tutar_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    literatur_ozeti = field.Integer(
        _(u"VERİLEN LİTERATÜR ÖZETİNİN PROJEYE UYGUNLUĞU VE YETERLİLİĞİ"),
        choices='bap_proje_degerlendirme_secenekler', default=1)

    literatur_ozeti_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    ozgun_deger = field.Integer(_(u"PROJENİN ÖZGÜN DEĞERİ"),
                                choices='bap_proje_degerlendirme_secenekler', default=1)

    ozgun_deger_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    yontem_amac_tutar = field.Integer(_(u"ÖNERİLEN YÖNTEMİN PROJE AMACI İLE TUTARLILIĞI"),
                                      choices='bap_proje_degerlendirme_secenekler', default=1)

    yontem_amac_tutar_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    yontem_uygulanabilirlik = field.Integer(_(u"ÖNERİLEN YÖNTEMİN UYGULANABİLİRLİĞİ"),
                                            choices='bap_proje_degerlendirme_secenekler', default=1)

    yontem_uygulanabilirlik_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    basari_olcut_gercek = field.Integer(_(u"BAŞARI ÖLÇÜTLERİNİN GERÇEKÇİLİĞİ"),
                                        choices='bap_proje_degerlendirme_secenekler', default=1)

    basari_olcut_gercek_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    katki_beklenti = field.Integer(_(u"PROJE İLE SAĞLANACAK KATKILARA İLİŞKİN BEKLENTİLER"),
                                        choices='bap_proje_degerlendirme_secenekler', default=1)

    katki_beklenti_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    bilim_endustri_katki = field.Integer(
        _(u"ARAŞTIRMA SONUÇLARININ BİLİME VE/VEYA ÜLKE ENDÜSTRİSİNE KATKISI"),
        choices='bap_proje_degerlendirme_secenekler', default=1)

    bilim_endustri_katki_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    arastirmaci_bilgi_yeterlilik = field.Integer(
        _(u"ARAŞTIRMACILARIN BİLGİ VE DENEYİM BİRİKİMİNİN YETERLİLİĞİ"),
        choices='bap_proje_degerlendirme_secenekler', default=1)

    arastirmaci_bilgi_yeterlilik_gerekce = field.Text(_(u"Gerekçe-Açıklama"))

    butce_gorus_oneri = field.Text(
        _(u"PROJENİN BÜTÇESİ VE UYGUNLUĞUNA İLİŞKİN GÖRÜŞ VE ÖNERİLERİNİZ"))

    proje_gorus_oneri = field.Text(
        _(u"PROJE İLE İLGİLİ UYARI VE ÖNERİLERİNİZ"))

    proje_degerlendirme_sonucu = field.Integer(
        _(u"DEĞERLENDİRME SONUCUNUZ"), choices='bap_proje_degerlendirme_sonuc', default=1)

    iptal = fields.Button(_(u"İptal"), cmd='iptal')
    tamam = fields.Button(_(u"Değerlendirme Kaydet"), cmd='kaydet')



class ProjeDegerlendirme(CrudView):
    """
        Proje hakemlerinin projeyi degerlendirirken kullanacagi is akisidir.
    """
    def proje_degerlendirme_karari_sor(self):
        """
            Hakemlik daveti gönderilen hakem adayına proje hakemlik daveti kararını soran
             adımdır. Hakem adayı proje özetini görüntüleyebilir, hakemlik davetini kabul ya da
             reddedebilir.
        """
        form = JsonForm(title=_(u"""%s Tarafından Gönderilen Hakemlik Daveti""" %
                                Personel.objects.get(user_id=self.current.task_data[
                                                         'davet_gonderen'].__unicode__())))
        form.help_text(_(u"""Proje özetini inceleyebilir, hakemlik davetini kabul edebilir ya da
        geri çevirebilirsiniz."""))
        form.ozet_incele = fields.Button(_(u"Proje Özeti İncele"), cmd='ozet_incele')
        form.davet_red = fields.Button(_(u"Hakemlik Davetini Reddet"), cmd='davet_red')
        form.davet_kabul = fields.Button(_(u"Hakemlik Davetini Kabul Et"), cmd='davet_kabul')

    def proje_ozet_goruntule(self):
        """
            Hakem adayına proje özetinin gösterildiği adımdır.
        """
        self.object = BAPProje.objects.get(self.current.task_data['bap_proje_id'])
        self.show()
        form = JsonForm()
        form.geri = fields.Button(_(u"Geri"))
        self.form_out(form)

    def red_bildirimi(self):
        proje = BAPProje.objects.get(self.current.task_data['bap_proje_id'])
        for degerlendirme in proje.ProjeDegerlendirmeleri:
            if degerlendirme.hakem().okutman().user_id == self.current.user_id:
                degerlendirme.hakem_degerlendirme_durumu = 4
        role = User.objects.get(self.current.task_data['davet_gonderen']).role_set[0].role
        role.send_notification(title=_(u"Proje Hakemlik Daveti Yanıtı"),
                               message=_(u"""%s adlı projeyi değerlendirmek üzere %s adlı hakem
                               adayına gönderdiğiniz davet reddedilmiştir. Proje listeleme adımından
                               hakemlik daveti butonuna tıklayarak yeniden davet gönderebilirsiniz.
                               """ % (proje.ad, self.current.user)),
                               typ=1,
                               sender=self.current.user
                               )

    def proje_degerlendir(self):
        form = ProjeDegerlendirmeForm()
        self.form_out(form)

    def degerlendirme_kaydet(self):
        pass
