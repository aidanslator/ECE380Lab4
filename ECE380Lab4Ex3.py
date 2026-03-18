#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from math import pi
import sip
import threading



class ECE380Lab4Ex3(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ECE380Lab4Ex3")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.f_dev_max = f_dev_max = 75000
        self.beta = beta = 5
        self.station_freq = station_freq = 250000
        self.samp_rate = samp_rate = 1000000
        self.audio_source = audio_source = 0
        self.audio_samp_rate = audio_samp_rate = 48000
        self.BW_Carson = BW_Carson = 2*f_dev_max*(1+1/beta)

        ##################################################
        # Blocks
        ##################################################

        # Create the options list
        self._audio_source_options = [0, 1]
        # Create the labels list
        self._audio_source_labels = ['WAV file', 'Tone']
        # Create the combo box
        self._audio_source_tool_bar = Qt.QToolBar(self)
        self._audio_source_tool_bar.addWidget(Qt.QLabel("Audio Source" + ": "))
        self._audio_source_combo_box = Qt.QComboBox()
        self._audio_source_tool_bar.addWidget(self._audio_source_combo_box)
        for _label in self._audio_source_labels: self._audio_source_combo_box.addItem(_label)
        self._audio_source_callback = lambda i: Qt.QMetaObject.invokeMethod(self._audio_source_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._audio_source_options.index(i)))
        self._audio_source_callback(self.audio_source)
        self._audio_source_combo_box.currentIndexChanged.connect(
            lambda i: self.set_audio_source(self._audio_source_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._audio_source_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=125,
                decimation=6,
                taps=[],
                fractional_bw=0.02)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            32768, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Transmitted Wideband FM', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 2, 2)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\aslator\\Downloads\\Intro_to_the_Universal_Declaration_of_Human_Rights_48k (1) (1).wav', True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,audio_source,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, station_freq, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_CONST_WAVE, (f_dev_max/beta), 1, 0, 0)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc((2*pi*f_dev_max/samp_rate))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ECE380Lab4Ex3")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_f_dev_max(self):
        return self.f_dev_max

    def set_f_dev_max(self, f_dev_max):
        self.f_dev_max = f_dev_max
        self.set_BW_Carson(2*self.f_dev_max*(1+1/self.beta))
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*pi*self.f_dev_max/self.samp_rate))
        self.analog_sig_source_x_0.set_frequency((self.f_dev_max/self.beta))

    def get_beta(self):
        return self.beta

    def set_beta(self, beta):
        self.beta = beta
        self.set_BW_Carson(2*self.f_dev_max*(1+1/self.beta))
        self.analog_sig_source_x_0.set_frequency((self.f_dev_max/self.beta))

    def get_station_freq(self):
        return self.station_freq

    def set_station_freq(self, station_freq):
        self.station_freq = station_freq
        self.analog_sig_source_x_1.set_frequency(self.station_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*pi*self.f_dev_max/self.samp_rate))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_audio_source(self):
        return self.audio_source

    def set_audio_source(self, audio_source):
        self.audio_source = audio_source
        self._audio_source_callback(self.audio_source)
        self.blocks_selector_0.set_input_index(self.audio_source)

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate

    def get_BW_Carson(self):
        return self.BW_Carson

    def set_BW_Carson(self, BW_Carson):
        self.BW_Carson = BW_Carson




def main(top_block_cls=ECE380Lab4Ex3, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
