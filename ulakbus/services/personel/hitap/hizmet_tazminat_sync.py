# -*-  coding: utf-8 -*-

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

"""HITAP Tazminat Senkronizasyon

Personelin Hitap'taki tazminat bilgilerinin
yereldeki kayıtlarla senkronizasyonunu yapar.

"""

from ulakbus.services.personel.hitap.hitap_sync import HITAPSync
from ulakbus.models.hitap import HizmetTazminat


class HizmetTazminatSync(HITAPSync):
    """
    HITAP Sync servisinden kalıtılmış Tazminat Bilgisi Senkronizasyon servisi

    """

    def handle(self):
        """
        Servis çağrıldığında tetiklenen metod.

        Attributes:
            sorgula_service (str): İlgili Hitap sorgu servisinin adı
            model (Model): Hitap'taki kaydın yereldeki karşılığı olan
                        ``HizmetTazminat`` modeli

        """

        self.sorgula_service = 'hizmet-tazminat-getir.hizmet-tazminat-getir'
        self.model = HizmetTazminat

        super(HizmetTazminatSync, self).handle()
