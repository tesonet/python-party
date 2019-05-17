"""Speed test for find.py"""
if __name__ == 'tests.test_speed':
#this is to prevent child processes to import additional modules they don't need.
    from find import soundex, find_words, get_results
    import unittest
    import time
    import os
    import multiprocessing
    from tests import SPEED_TEST
    import matplotlib.pyplot as plt

    def time_it(filepath, keyword, workers, chunk_size):
        """Main method rewritten for testing speed"""
        #Click invoker is not good for testing as it adds execution time and memory
        start = time.time()
        keyword = soundex(keyword)
        #Different default chunk size for single/multi process
        if not chunk_size:
            if not workers or workers == 1:
                chunk_size = 2
            else:
                chunk_size = 128

        #Set up pool if more than 1 workers selected
        if workers < 1:
            pool = None
        else:
            multiprocessing.set_start_method('spawn', force=True)
            pool = multiprocessing.Pool(workers)

        #Translate to bytes
        chunk_size *= 1024

        #Read file>get words->soundex->score->sort
        words = find_words(filepath, chunk_size, None, pool)
        _ = get_results(words, keyword[1])

        end = time.time()-start

        return round(end, 4)

    def gen_large_file(ntimes):
        """generate 100MB of txt"""
        file_path = f'tests/test_data/_temp{ntimes*100}MB.txt'
        with open(file_path, 'w+',encoding='utf8') as outfile:
            with open('tests/test_data/plague_of_pythons.txt','r',encoding='utf8') as infile:
                for line in infile:
                    for _ in range(414*ntimes):
                        outfile.write(line)
        return file_path

    def clean_up():
        """Delete temp files"""
        for filename in os.listdir('tests/test_data'):
            if filename.startswith('_temp'):
                os.remove("tests/test_data/"+filename)


    @unittest.skipIf(not SPEED_TEST, "User skipped this test")
    class TestSpeed(unittest.TestCase):
        """Tests speed."""
        def test_speed(self):
            """Test speed,plot and log"""
            size= 1 #*100 MB
            chunk_sizes = [128, 256, 512, 1024]
            workers = [2, 4, 8]
            runs = 3

            large_file = gen_large_file(size)
            results = {}

            for num_work in workers:
                avarage = []
                for chunk_size in chunk_sizes:
                    test_time = []
                    for _ in range(runs):
                        test_time.append(time_it(large_file, 'test', num_work, chunk_size))
                    avarage.append(sum(test_time)/len(test_time))
                results[num_work] = avarage

            with open('tests/test_data/test_speed_log.txt', 'w+',encoding='utf8') as file_obj:
                file_obj.write(f'Avarage time of {runs} runs:\n')
                file_obj.write(f'Workers:__' + '>>>'+ f'time for {chunk_sizes} chunk size' + '\n\n')
                for key, val in results.items():
                    file_obj.write(f'Workers: {str(key)}' + ' >>> '+ str(val) + '\n\n')

            for num_work in results:
                plt.plot(chunk_sizes, results[num_work], 'o-', label=f'Num_work:{num_work}')
            plt.xlabel('chunk size(kb)')
            plt.ylabel('time(s)')
            plt.legend()
            plt.title(f'{size*100}MB file test')
            plt.savefig('tests/test_data/test_speed_plot.png')
            clean_up()
            self.assertIn('test_speed_log.txt', os.listdir('tests/test_data'))
            self.assertIn('test_speed_plot.png', os.listdir('tests/test_data'))
            print("\nSpeed test log and plot saved in /tests/test/data.")
