
cp /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/CAST.fits /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/
cp /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/ModTab.fits /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/
cp /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/ModTabModels.fits /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/
cp /home/ameert/git_projects/catalog2013/data_tables.pdf /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/Meert2014_v1/

cd /home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/

tar -czvf Meert2014_v1.tgz Meert2014_v1 

cd -