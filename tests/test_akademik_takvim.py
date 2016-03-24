# -*-  coding: utf-8 -*-
#
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.


import time
from ulakbus.models.auth import User
from ulakbus.models.ogrenci import AKADEMIK_TAKVIM_ETKINLIKLERI
from ulakbus.models.ogrenci import AkademikTakvim
from zengine.lib.test_utils import BaseTestCase


class TestCase(BaseTestCase):
    """
    Bu sınıf ``BaseTestCase`` extend edilerek hazırlanmıştır.

    """

    def test_academic_calendar(self):
        """
        Adalet Meslek Yüksekokulu Öğrencisi rolüne sahip test_user adlı kullanıcı giriş yaptığında,
        xxxxxxxxxxxxxx keyine sahip rektörlüğe ait akademik takvimi görmesi beklenir.
        Çünkü bölümüne veya fakültesine ait bir akademik takvim tanımlanmamıştır.

        Bu iş akışı ilk adımda rektörlüğe ait akademik takvim kayıtlarını listeler.

        Veritabanından çekilen akademik takvim kayıtlarının sayısı ile sunucudan dönen akademik takvim
        kayıtlarının sayısı karşılastırılıp test edilir.

        Akademik takvim kaydının nesnelerinden biri seçilir, seçilen nesnenin etkinliği, başlangıcı ve
        bitişi sunucudan dönen etkinlik, başlangıç ve bitiş kayıtlarıyla karşılaştırılıp test edilir.

        test_user adlı kullanıcıya çıkış yaptırılır.

        Kamu Hukuku Bölümü öğrencisi rolüne sahip onur adlı kullanıcı giriş yaptığında, xxxxxxxxxx keyine sahip
        Kamu Hukuku Bölümü akademik takvimi görmesi beklenir.Çünkü kendi bölümüne ait tanımlı akademik takvim vardır.

        Bu iş akışı ilk adımda eğitim fakültesine ait akademik takvim kayıtlarını listeler.

        Veritabanından çekilen akademik takvim kayıtlarının sayısı ile sunucudan dönen akademik takvim
        kayıtlarının sayısı karşılastırılıp test edilir.

        Akademik takvim kaydının nesnelerinden biri seçilir, seçilen nesnenin etkinliği, başlangıcı ve
        bitişi sunucudan dönen etkinlik, başlangıç ve bitiş kayıtlarıyla karşılaştırılır.

        """

        # Veritabınından test_user adlı kullanıcı seçilir.
        # Kullanıcıya login yaptırılır.
        self.prepare_client('/akademik_takvim', username='test_user')
        resp = self.client.post()

        # Birimin kayıtlı olduğu akademik takvim kayıtını getirir.
        akademik_takvim = AkademikTakvim.objects.get(birim_id='CcKtz93YvvBBfEAfNpRn9Aazrzz')

        # Sunucudan dönen akademik takvim kayıtları ile veritabanından çekilen akademik kayıtları
        # karşılaştırılıp test edilir
        assert len(akademik_takvim.Takvim) == len(resp.json['object']['fields'])

        # Akademik takvim kaydının nesnelerinden biri seçilir.
        takvim = akademik_takvim.Takvim[3]
        # Takvim kaydının etkinliğini getirir.
        etkinlik = takvim.etkinlik

        assert dict(AKADEMIK_TAKVIM_ETKINLIKLERI).get(str(etkinlik), '') == \
               resp.json['object']['fields'][etkinlik - 1][
                   'Etkinlik']
        assert takvim.baslangic.strftime('%d.%m.%Y') == resp.json['object']['fields'][etkinlik - 1][
            u'Başlangıç']
        assert takvim.bitis.strftime('%d.%m.%Y') == resp.json['object']['fields'][etkinlik - 1][
            u'Bitiş']

        # Kullanıcıya çıkış yaptırılır.
        self.client.set_path('/logout')
        self.client.post()

        # Veritabınından onur adlı kullanıcı seçilir.

        time.sleep(1)

        # Kullanıcıya login yaptırılır.
        usr = User.objects.get(username='onur')
        self.prepare_client('/akademik_takvim', user=usr)
        response = self.client.post()

        # Rol'ün kayıtlı olduğu birim getirilir.
        unit = usr.role_set[0].role.unit

        # Birimin kayıtlı olduğu akademik takvim kayıtını getirir.
        akademik_takvim = AkademikTakvim.objects.get(birim_id=unit.key)

        # Sunucudan dönen akademik takvim kayıtları ile veritabanından çekilen akademik kayıtları
        # karşılaştırılıp test edilir.
        assert len(akademik_takvim.Takvim) == len(response.json['object']['fields'])

        # Akademik takvim kaydının nesnelerinden biri seçilir.
        takvim = akademik_takvim.Takvim[0]
        # Takvim kaydının etkinliğini getirir.
        etkinlik = takvim.etkinlik

        assert response.json['object']['fields'][0]['Etkinlik'] == dict(
            AKADEMIK_TAKVIM_ETKINLIKLERI).get(
            str(etkinlik), '')
        assert response.json['object']['fields'][0][u'Başlangıç'] == takvim.baslangic.strftime(
            '%d.%m.%Y')
        assert response.json['object']['fields'][0][u'Bitiş'] == takvim.bitis.strftime('%d.%m.%Y')