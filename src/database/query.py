def ql_cari_rs(kabupaten, provinsi, nama_poli):
    query = f'''
    SELECT DISTINCT
        rs.id AS id_rs,
        p.id AS id_poli,
        rs.nama_rs,
        p.nama_poli
    FROM tb_rs rs
    JOIN tb_poli p ON rs.id = p.id_rs
    WHERE rs.kabupaten = '{kabupaten}' AND rs.provinsi = '{provinsi}' AND nama_poli = '{nama_poli}';
    '''
    return query

def ql_cari_dokter(rumah_sakit, nama_poli):
    query = f'''
    SELECT 
        d.id AS id_dokter,
        d.nama_dokter
    FROM tb_dokter d
    JOIN tb_rs rs ON d.id_rs = rs.id
    JOIN tb_poli p ON d.id_poli = p.id
    WHERE rs.nama_rs = '{rumah_sakit}' 
    AND p.nama_poli = '{nama_poli}';
    '''
    return query

def ql_cari_hari_dan_jam(nama_dokter, rumah_sakit, nama_poli):
    query = f'''
    SELECT 
    pr.id AS id_praktek,
    pr.hari_praktek,
    TO_CHAR(pr.jam_praktek, 'HH24:MI') as jam_praktek,
    d.nama_dokter
    FROM tb_praktek pr
    JOIN tb_dokter d ON pr.id_dokter = d.id
    JOIN tb_rs rs ON d.id_rs = rs.id
    JOIN tb_poli p ON d.id_poli = p.id
    WHERE d.nama_dokter = '{nama_dokter}'
        AND rs.nama_rs = '{rumah_sakit}'
        AND p.nama_poli = '{nama_poli}'
    ORDER BY 
        CASE 
            WHEN hari_praktek = 'Senin' THEN 1
            WHEN hari_praktek = 'Selasa' THEN 2
            WHEN hari_praktek = 'Rabu' THEN 3
            WHEN hari_praktek = 'Kamis' THEN 4
            WHEN hari_praktek = 'Jumat' THEN 5
            WHEN hari_praktek = 'Sabtu' THEN 6
            WHEN hari_praktek = 'Minggu' THEN 7
        END,
        pr.jam_praktek;
    '''
    return query

def ql_simpan_data(kimlik, nama_lengkap, umur, gender, kabupaten, provinsi, 
                gejala, id_poli, id_rs, id_dokter, id_praktek):
    query = f'''
    INSERT INTO tb_pasien (kimlik, nama_lengkap, umur, gender, kabupaten, provinsi, gejala, id_poli, id_rs, id_dokter, id_praktek) VALUES (
        '{kimlik}',            -- kimlik (contoh nomor KTP)
        '{nama_lengkap}',               -- nama_lengkap
        {umur},                    -- umur
        '{gender}',
        '{kabupaten}',                    -- kabupaten
        '{provinsi}',                 -- provinsi
        '{gejala}',                   -- gejala
        {id_poli},                            -- id_poli (sesuaikan dengan id poli yang ada)
        {id_rs},                            -- id_rs (sesuaikan dengan id RS yang ada)
        {id_dokter},                            -- id_dokter (sesuaikan dengan id dokter yang ada)
        {id_praktek}                             -- id_praktek (sesuaikan dengan id praktek yang ada)
    );
    '''
    return query

def template_email(kimlik, nama_lengkap, umur, gender, nama_rumah_sakit, nama_poli, nama_dokter, hari_praktek, jam_praktek):
    return f"""
    Terima kasih telah mendaftarkan diri di sistem SEHAT.
    Berikut adalah rincian data pasien:
    1. Nomor Identitas: {kimlik}
    2. Nama Lengkap: {nama_lengkap}
    3. Umur: {umur}
    4. Gender: {gender}
    5. Rumah Sakit yang dipilih: {nama_rumah_sakit}
    6. Poli yang dipilih: {nama_poli}
    7. Dokter yang dipilih: {nama_dokter}
    8. Hari dan Jam Praktek: {hari_praktek}, {jam_praktek}
    
    Semoga lekas sembuh dan semoga dapat beraktivitas sedia kala.
    ASEP Team
    """