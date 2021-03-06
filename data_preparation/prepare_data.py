from __future__ import print_function
import argparse
import os
import sys
import subprocess
import pdb

def get_formatted_time(seconds):
    microsecond = str(seconds - int(seconds)).split('.')[-1]
    int_seconds = int(seconds)
    hour = int_seconds // 3600
    minute = (int_seconds - hour * 3600) // 60
    second = int_seconds - hour * 3600 - minute * 60
    return "{:02}:{:02}:{:02}.".format(hour, minute, second) + microsecond[0:6]

def dl_youtube(link, target_file):
    p = subprocess.Popen(["youtube-dl",
                          "-f", "best",
                          "--merge-output-format", "mp4",
                          "--restrict-filenames",
                          "--socket-timeout", "20",
                          "-iwc",
                          "--write-info-json",
                          '--write-annotations',
                          '--prefer-ffmpeg',
                          link,
                          '-o', target_file],
                         )
    out, err = p.communicate()

def prepare_data(file, target_dir):

    temp_directory = os.path.abspath(os.path.join(target_dir, "youtube_videos_temp"))
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)
    with open(file) as f:
        next(f)
        for l in f:
            l = l.strip()
            if len(l) > 0:
                link, start, end, video, utterance = l.split(',')[:5]
                if video == 'a1b44e5f3':
                    pdb.set_trace()
                    print(video+'is extracting...')
                result_dir = os.path.join(os.path.join(target_dir, video))
                if not os.path.exists(result_dir):
                    os.makedirs(result_dir)
                result_filename = os.path.abspath(os.path.join(result_dir, utterance))
                #dl video with youtube-dl
                target_file = os.path.abspath(os.path.join(temp_directory, video + ".mp4"))
                if not os.path.exists(target_file):
                    dl_youtube(link, target_file)
                if not os.path.exists(result_filename):
                    p = subprocess.call(["ffmpeg",
                                     "-y",
                                     "-i", target_file,
                                     "-ss", get_formatted_time(float(start)),
                                     #"-c:v", "libx264",
                                     "-vcodec", "libx264",
                                     "-preset", "superfast",
                                     "-f", "mp4",
                                     "-c:a", "aac",
                                     "-to", get_formatted_time(float(end)),
                                     '-strict', '-2',
                                     result_filename],
                                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--split-file", help = "Metadata file")
    parser.add_argument("--target-dir")
    opt = parser.parse_args()
    if not os.path.exists(opt.split_file):
        print("Cannot find split file")
        sys.exit(-1)
    if not os.path.exists(opt.target_dir):
        os.makedirs(opt.target_dir)
    else:
        print("Target dir already exists.")

    prepare_data(opt.split_file, opt.target_dir)
