
cp /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/UPenn_PhotDec_CAST.fits /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/
cp /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/UPenn_PhotDec_Models_rband.fits /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/
cp /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/UPenn_PhotDec_nonParam_rband.fits /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/
cp /home/ameert/git_projects/catalog2013/data_tables.pdf /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/

cd /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/

tar -czvf Meert2014_v1.tgz Meert2014_v1 

cd -