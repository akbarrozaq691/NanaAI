from src.database.database import read_db
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from src.database.query import *
from src.email.send_email import send_email

db = read_db()

class InputCariRS(BaseModel):
    kabupaten: str = Field(description="nama kabupaten")
    provinsi: str = Field(description="nama provinsi")
    nama_poli: str = Field(description="nama poli")

class InputCariDokter(BaseModel):
    rumah_sakit: str = Field(description="nama rumah sakit")
    nama_poli: str = Field(description="nama poli")

class InputCariHariKerja(BaseModel):
    nama_dokter: str = Field(description="nama dokter")
    rumah_sakit: str = Field(description="nama rumah sakit")
    nama_poli: str = Field(description="nama poli")

class InputSimpanData(BaseModel):
    kimlik: str = Field(description="nomor kimlik")
    nama_lengkap: str = Field(description="nama lengkap")
    umur: str = Field(description="umur")
    gender: str = Field(description="gender")
    kabupaten: str = Field(description="nama kabupaten")
    provinsi: str = Field(description="nama provinsi")
    gejala: str = Field(description="gejala")
    id_poli: str = Field(description="id poli")
    id_rs: str = Field(description="id rumah sakit")
    id_dokter: str = Field(description="id dokter")
    id_praktek: str = Field(description="id praktek")

class InputPenerima(BaseModel):
    email_penerima: str = Field(description="email penerima")
    kimlik: str = Field(description="nomor kimlik")
    nama_lengkap: str = Field(description="nama lengkap")
    umur: str = Field(description="umur")
    gender: str = Field(description="gender")
    nama_dokter: str = Field(description="nama dokter")
    nama_rumah_sakit: str = Field(description="nama rumah sakit")
    nama_poli: str = Field(description="nama poli")
    hari_praktek: str = Field(description="hari praktek")
    jam_praktek: str = Field(description="jam praktek")

def query_cari_rs(kabupaten: str, provinsi: str, nama_poli: str) -> str:
    """
    Gunakan query berikut untuk memberikan daftar rumah sakit berdasarkan kabupaten, provinsi, dan poli.
    """
    query = ql_cari_rs(kabupaten, provinsi, nama_poli)
    return db.run(query, include_columns=True)

def query_cari_dokter(rumah_sakit: str, nama_poli: str) -> str:
    """
    Gunakan query berikut untuk memberikan daftar dokter berdasarkan rumah sakit dan poli.
    """
    query = ql_cari_dokter(rumah_sakit, nama_poli)
    return db.run(query, include_columns=True)

def query_cari_hari_dan_jam(nama_dokter: str, rumah_sakit: str, nama_poli: str) -> str:
    """
    Gunakan query berikut untuk memberikan daftar hari dan jam berdasarkan nama dokter, rumah sakit, dan poli.
    """
    query = ql_cari_hari_dan_jam(nama_dokter, rumah_sakit, nama_poli)
    return db.run(query, include_columns=True)

def query_simpan_data(kimlik: str, nama_lengkap: str, umur: str, gender: str, kabupaten: str, provinsi: str, 
                gejala: str, id_poli: str, id_rs: str, id_dokter:str, id_praktek: str) -> str:
    """
    Gunakan query berikut untuk simpan data pasien.
    """
    query = ql_simpan_data(kimlik, nama_lengkap, umur, gender,
                           kabupaten, provinsi, gejala, id_poli, 
                           id_rs, id_dokter, id_praktek)
    return db.run(query, include_columns=False)

def kirim_email(email_penerima: str, kimlik: str, nama_lengkap: str, umur: str, 
                gender: str, nama_rumah_sakit: str, nama_poli: str,
                nama_dokter: str, hari_praktek: str, jam_praktek: str) -> str:
    """
    Gunakan fungsi ini untuk mengirim email ke penerima.
    """
    template_email_fix = template_email(kimlik, nama_lengkap, umur, gender, nama_rumah_sakit,
                                         nama_poli, nama_dokter, hari_praktek, jam_praktek)
    _, message = send_email(email_penerima, template_email_fix)
    return message
    

def custom_query_pasien():
    tools = [
        StructuredTool.from_function(
            func=query_cari_rs,
            name='query_cari_rs',
            description='tools untuk cari rumah sakit',
            args_schema=InputCariRS,
            return_direct=False
        ),
        StructuredTool.from_function(
            func=query_cari_dokter,
            name='query_cari_dokter',
            description='tools untuk cari dokter',
            args_schema=InputCariDokter,
            return_direct=False
        ),
        StructuredTool.from_function(
            func=query_cari_hari_dan_jam,
            name='query_cari_hari_dan_jam',
            description='tools untuk cari hari dan jam dokter',
            args_schema=InputCariHariKerja,
            return_direct=False
        ),
        StructuredTool.from_function(
            func=query_simpan_data,
            name='query_simpan_data',
            description='tools untuk simpan data pasien',
            args_schema=InputSimpanData,
            return_direct=False
        ),
        StructuredTool.from_function(
            func=kirim_email,
            name='kirim_email',
            description='tools untuk mengirim email untuk pasien',
            args_schema=InputPenerima,
            return_direct=False
        )
    ]
    return tools