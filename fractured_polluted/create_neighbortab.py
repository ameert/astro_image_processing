insert into i_deep_neighbors_ser (galcount, neighbornum, xctr_bulge, yctr_bulge, m_bulge, r_bulge, n_bulge, ba_bulge, pa_bulge, ismatched) select a.galcount, a.neighbornum, a.xctr, a.yctr, a.m_ser - 25.256 -c.aa_i-c.kk_i*c.airmass_i, a.r_ser*0.396, a.n_ser, a.ba_ser, a.pa_ser, 0 from deep_i_ser_neighborvals as a,  i_band_ser as b, CAST as c where a.galcount = b.galcount and b.galcount = c.galcount;


